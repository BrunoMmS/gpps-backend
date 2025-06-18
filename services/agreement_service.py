from typing import List, Optional
from sqlalchemy.orm import Session
from cruds.agreementDAO import AgreementDAO
from entities.agreement_entity import AgreementEntity, AgreementStatus
from entities.user_entity import UserEntity
from schemas.agreements_schema import AgreementCreate, AgreementUpdate, AgreementResponse, AgreementWithUser
from schemas.project_schema import ProyectComplete
from models.agreement_model import AgreementModel
from schemas.user_schema import User
from services.user_service import UserService
from services.project_service import ProjectService
from roles.rol import Rol
from services.notification_service import NotificationService


class AgreementService:

    def __init__(self, agreement_dao=None, user_service=None, project_service=None):
        self.agreement_dao = agreement_dao or AgreementDAO()
        self.user_service = user_service or UserService()
        self.project_service = project_service or ProjectService()

    # =====================================================
    # MÉTODOS PÚBLICOS - OPERACIONES PRINCIPALES
    # =====================================================

    def create_agreement(self, db: Session, data: AgreementCreate, creator_id: int) -> AgreementResponse:
        creator_entity = self._get_user_entity(db, creator_id)
        assigned_entity = None

        if data.user_id and data.user_id != creator_id:
            assigned_entity = self._get_user_entity(db, data.user_id)
            self._validate_assignment_roles(creator_entity, assigned_entity)

        self._validate_creation_roles(creator_entity, assigned_entity)

        agreement_entity = AgreementEntity(
            start_date=data.start_date,
            end_date=data.end_date,
            created_by=creator_id,
            user_id=data.user_id,
            status=AgreementStatus.PENDING
        )

        if assigned_entity:
            agreement_entity.assign_user_id(assigned_entity)

        db_agreement = self.agreement_dao.create(db, agreement_entity)

        if data.user_id and data.user_id != creator_id:
            self._notify_agreement_creation(db, data.user_id, db_agreement.id)

        return self._model_to_schema(db_agreement)

    def update_agreement(self, db: Session, agreement_id: int, data: AgreementUpdate, updater_id: int) -> AgreementResponse:
        updater = self._get_and_validate_user(db, updater_id)
        self._validate_admin_permissions(updater, "actualizar convenios")

        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        agreement_entity = self._model_to_entity(db_agreement)

        new_start = data.start_date or agreement_entity.get_start_date
        new_end = data.end_date or agreement_entity.get_end_date
        agreement_entity.update_dates(new_start, new_end)

        if data.status:
            agreement_entity.update_status(data.status)

        if data.user_id:
            user_entity = self._get_user_entity(db, data.user_id)
            self._validate_assignment_roles(self._user_to_entity(updater), user_entity, db_agreement.created_by, updater_id)
            agreement_entity.assign_user_id(user_entity)

        if data.project_id:
            self._validate_project_exists(db, data.project_id)

        updated_agreement = self.agreement_dao.update(db, agreement_entity)
        return self._model_to_schema(updated_agreement)

    def approve_agreement(self, db: Session, agreement_id: int, approved_by_id: int) -> AgreementResponse:
        user_entity = self._get_user_entity(db, approved_by_id)
        return self._change_agreement_status(db, agreement_id, user_entity, "approve")

    def reject_agreement(self, db: Session, agreement_id: int, rejected_by_id: int) -> AgreementResponse:
        user_entity = self._get_user_entity(db, rejected_by_id)
        return self._change_agreement_status(db, agreement_id, user_entity, "reject")

    def assign_user_to_agreement(self, db: Session, agreement_id: int, user_id: int, assigner_id: int) -> AgreementResponse:
        assigner_entity = self._get_user_entity(db, assigner_id)
        user_entity = self._get_user_entity(db, user_id)

        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        self._validate_assignment_roles(assigner_entity, user_entity, db_agreement.created_by, assigner_id)

        agreement_entity = self._model_to_entity(db_agreement)
        agreement_entity.assign_user_id(user_entity)

        updated_agreement = self.agreement_dao.update(db, agreement_entity)
        self._notify_external_assignment(db, user_id, agreement_id)
        return self._model_to_schema(updated_agreement)

    def assign_project_to_agreement(self, db: Session, agreement_id: int, project_id: int, assigner_id: int) -> AgreementResponse:
        assigner = self._get_and_validate_user(db, assigner_id)
        self._validate_admin_permissions(assigner, "asignar proyectos a convenios")

        self._validate_project_exists(db, project_id)

        updated_agreement = self.agreement_dao.assign_project(db, agreement_id, project_id)
        if not updated_agreement:
            raise ValueError(f"No se encontró el convenio con ID {agreement_id}")

        return self._model_to_schema(updated_agreement)

    def delete_agreement(self, db: Session, agreement_id: int, deleter_id: int) -> bool:
        deleter = self._get_and_validate_user(db, deleter_id)
        self._validate_admin_permissions(deleter, "eliminar convenios")

        success = self.agreement_dao.delete(db, agreement_id)
        if not success:
            raise ValueError("No se encontró el convenio para eliminar.")
        return success

    # =====================================================
    # MÉTODOS DE CONSULTA
    # =====================================================

    def get_agreement_by_id(self, db: Session, agreement_id: int) -> AgreementResponse:
        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        return self._model_to_schema(db_agreement)

    def list_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar todos los convenios")
        db_agreements = self.agreement_dao.list(db)
        return [self._model_to_schema(a) for a in db_agreements]
    
    def list_agreement_with_project(self, db: Session, agreement_id: int, requester_id: int) -> ProyectComplete:
        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar convenios por proyecto")
        agreement = self.get_agreement_by_id(db, agreement_id)
        project_id = agreement.project_id    
        project_data = self.project_service.get_complete_project(db, project_id)
        return project_data

    def list_agreements_by_creator(self, db: Session, creator_id: int, requester_id: Optional[int] = None) -> List[AgreementResponse]:
        if requester_id is not None and creator_id != requester_id:
            requester = self._get_and_validate_user(db, requester_id)
            self._validate_admin_permissions(requester, "listar convenios por creador")

        agreements = self.agreement_dao.list(db)
        filtered = [a for a in agreements if a.created_by == creator_id]
        return [self._model_to_schema(a) for a in filtered]

    def list_pending_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar convenios pendientes")
        db_agreements = self.agreement_dao.get_by_status(db, AgreementStatus.PENDING)
        return [self._model_to_schema(a) for a in db_agreements]

    def list_user_agreements(self, db: Session, user_id: int, requester_id: int) -> List[AgreementResponse]:
        requester = self._get_and_validate_user(db, requester_id)
        if requester_id != user_id:
            self._validate_admin_permissions(requester, "listar convenios de otros usuarios")

        all_agreements = self.agreement_dao.list(db)
        user_agreements = [a for a in all_agreements if a.user_id == user_id]
        return [self._model_to_schema(a) for a in user_agreements]

    def get_current_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar convenios vigentes")
        agreements = self.agreement_dao.list(db)
        return [self._model_to_schema(a) for a in agreements if a.is_current()]

    def get_expired_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar convenios expirados")
        agreements = self.agreement_dao.list(db)
        return [self._model_to_schema(a) for a in agreements if a.is_expired()]

    # =====================================================
    # MÉTODOS PRIVADOS - UTILIDADES Y VALIDACIONES
    # =====================================================

    def _get_user_entity(self, db: Session, user_id: int):
        return self._user_to_entity(self._get_and_validate_user(db, user_id))

    def _get_and_validate_user(self, db: Session, user_id: int):
        try:
            return self.user_service.get_user_by_id(db, user_id)
        except ValueError:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")

    def _validate_project_exists(self, db: Session, project_id: int):
        try:
            self.project_service.get_project_with_user(db, project_id)
        except ValueError:
            raise ValueError(f"El proyecto con ID {project_id} no existe")

    def _validate_creation_roles(self, creator_entity, assigned_entity=None):
        if creator_entity.getRole() not in [Rol.admin, Rol.exEntity]:
            raise ValueError("Solo administradores y entidades externas pueden crear convenios.")
        if assigned_entity:
            self._validate_assignment_roles(creator_entity, assigned_entity)

    def _validate_assignment_roles(self, assigner_entity, assigned_entity, created_by: Optional[int] = None, assigner_id: Optional[int] = None):
        if assigner_entity.getRole() == Rol.admin:
            if assigned_entity.getRole() != Rol.exEntity:
                raise ValueError("Un administrador solo puede asignar una entidad externa al convenio.")
        elif assigner_entity.getRole() == Rol.exEntity:
            if assigned_entity.getRole() != Rol.admin:
                raise ValueError("Una entidad externa solo puede asignar un administrador al convenio.")
            if created_by and assigner_id and created_by != assigner_id:
                raise ValueError("Solo la entidad externa que creó el convenio puede asignar un administrador.")
        else:
            raise ValueError("No tienes permisos para asignar usuarios a convenios.")

    def _get_agreement_or_raise(self, db: Session, agreement_id: int) -> AgreementModel:
        agreement = self.agreement_dao.get_by_id(db, agreement_id)
        if not agreement:
            raise ValueError(f"Convenio con ID {agreement_id} no encontrado")
        return agreement

    def _validate_admin_permissions(self, user, action: str) -> None:
        if self._user_to_entity(user).getRole() not in [Rol.admin, Rol.exEntity]:
            raise ValueError(f"No tienes permisos para {action}.")

    def _change_agreement_status(self, db: Session, agreement_id: int, user_entity, action: str) -> AgreementResponse:
        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        entity = self._model_to_entity(db_agreement)

        if action == "approve":
            entity.approve(user_entity)
            self._notify_agreement_approval(db, db_agreement.user_id, agreement_id)
        elif action == "reject":
            entity.reject(user_entity)
            self._notify_agreement_rejection(db, db_agreement.user_id, agreement_id)
        else:
            raise ValueError("Acción no válida para cambio de estado")

        updated = self.agreement_dao.update(db, entity)
        return self._model_to_schema(updated)

    def _user_to_entity(self, user):
        return self.user_service.to_entity(user)

    def _model_to_schema(self, model: AgreementModel) -> AgreementResponse:
        return AgreementResponse(
            id=model.id,
            start_date=model.start_date,
            end_date=model.end_date,
            current=model.is_current(),
            created_by=model.created_by,
            user_id=model.user_id,
            project_id=model.project_id,
            status=AgreementStatus(model.status)
        )
    
    def _model_toschema_with_user(self, model: AgreementModel) -> List[AgreementWithUser]:
        user_entity: UserEntity = self.user_service.get_user_by_id(model.user_id) if model.user_id else None
        user_schema = User(user_entity.getId(), 
                           user_entity.getUsername(), 
                           user_entity.getLastname(), 
                           user_entity.getEmail(), 
                           user_entity.getRole()) if user_entity else None

        return AgreementWithUser(
            id=model.id,
            start_date=model.start_date,
            end_date=model.end_date,
            current=model.is_current(),
            created_by=model.created_by,
            user_id=user_schema,
            project_id=model.project_id,
            status=AgreementStatus(model.status)
        )

    def _model_to_entity(self, model: AgreementModel) -> AgreementEntity:
        return AgreementEntity(
            id=model.id,
            start_date=model.start_date,
            end_date=model.end_date,
            user_id=model.user_id,
            project_id=model.project_id,
            status=AgreementStatus(model.status),
            created_by=model.created_by
        )
    
    
    def get_all_agreements_with_user(self, db: Session, user_id: int) -> List[AgreementWithUser]:
        user = self.user_service.get_user_by_id(db, user_id)
        agreements: List[AgreementModel] = self.agreement_dao.list(db)
        agreements_schemas: List[AgreementWithUser]  = []
 
        for agreement in agreements:
            agreements_schemas.append(AgreementWithUser(
            id=agreement.id,
            start_date=agreement.start_date,
            end_date=agreement.end_date,
            created_by=agreement.created_by,
            user_id=User(
                id=user.id,
                username=user.username,
                lastname=user.lastname,
                email=user.email,
                role=user.role
            ) if user else None,
            project_id=agreement.project_id,
            status=AgreementStatus(agreement.status)
        ))

    # =====================================================
    # MÉTODOS DE NOTIFICACIÓN
    # =====================================================

    def _notify_agreement_creation(self, db: Session, user_id: int, agreement_id: int) -> None:
        try:
            NotificationService(db).notify(user_id, f"Se ha creado un nuevo convenio asociado a tu cuenta.")
        except Exception:
            pass

    def _notify_agreement_approval(self, db: Session, user_id: int, agreement_id: int) -> None:
        try:
            NotificationService(db).notify(user_id, f"Tu convenio con ID {agreement_id} ha sido aprobado.")
        except Exception:
            pass

    def _notify_agreement_rejection(self, db: Session, user_id: int, agreement_id: int) -> None:
        try:
            NotificationService(db).notify(user_id, f"Tu convenio con ID {agreement_id} ha sido rechazado.")
        except Exception:
            pass

    def _notify_external_assignment(self, db: Session, user_id: int, agreement_id: int) -> None:
        try:
            NotificationService(db).notify(user_id, f"Has sido asignado como representante externo del convenio con ID {agreement_id}.")
        except Exception:
            pass
