from typing import List, Optional
from sqlalchemy.orm import Session
from cruds.agreementDAO import AgreementDAO
from entities.agreement_entity import AgreementEntity, AgreementStatus
from schemas.agreements_schema import AgreementCreate, AgreementUpdate, AgreementResponse
from schemas.project_schema import ProyectComplete
from models.agreement_model import AgreementModel
from services.user_service import UserService
from services.project_service import ProjectService
from services.rol import Rol
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
        # Crea un nuevo convenio. Solo pueden crear convenios: Administradores y Entidades Externas

        creator = self._get_and_validate_user(db, creator_id)
        self._validate_permissions(creator)

        agreement_entity = AgreementEntity(
            start_date=data.start_date,
            end_date=data.end_date,
            user_id=data.user_id,
            status=AgreementStatus.PENDING
        )

        if data.user_id:
            user = self._get_and_validate_user(db, data.user_id)
            agreement_entity.assign_user_id(self._user_to_entity(user))

        db_agreement = self.agreement_dao.create(db, agreement_entity)

        if data.user_id and data.user_id != creator_id:
            self._notify_agreement_creation(db, data.user_id, db_agreement.id)

        return self._model_to_schema(db_agreement)

    def update_agreement(self, db: Session, agreement_id: int, data: AgreementUpdate, updater_id: int) -> AgreementResponse:
        # Actualiza un convenio existente

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
            user = self._get_and_validate_user(db, data.user_id)
            agreement_entity.assign_user_id(self._user_to_entity(user))

        if data.project_id:
            try:
                self.project_service.get_project_with_user(db, data.project_id)
            except ValueError:
                raise ValueError(f"El proyecto con ID {data.project_id} no existe")

        updated_agreement = self.agreement_dao.update(db, agreement_entity)
        return self._model_to_schema(updated_agreement)

    def approve_agreement(self, db: Session, agreement_id: int, approved_by_id: int) -> AgreementResponse:
        # Aprueba un convenio
        user = self._get_and_validate_user(db, approved_by_id)
        return self._change_agreement_status(db, agreement_id, self._user_to_entity(user), "approve")

    def reject_agreement(self, db: Session, agreement_id: int, rejected_by_id: int) -> AgreementResponse:
        # Rechaza un convenio
        user = self._get_and_validate_user(db, rejected_by_id)
        return self._change_agreement_status(db, agreement_id, self._user_to_entity(user), "reject")

    def assign_user_to_agreement(self, db: Session, agreement_id: int, user_id: int, assigner_id: int) -> AgreementResponse:
        # Permite asignar un usuario a un convenio bajo la siguiente regla:
        # Si el asignador es ADMINISTRADOR, puede asignar una ENTIDAD EXTERNA.
        # Si el asignador es ENTIDAD EXTERNA, puede asignar un ADMINISTRADOR.

        assigner = self._get_and_validate_user(db, assigner_id)
        assigner_entity = self._user_to_entity(assigner)

        user = self._get_and_validate_user(db, user_id)
        user_entity = self._user_to_entity(user)

        if assigner_entity.getRole() == Rol.admin:
            if user_entity.getRole() != Rol.exEntity:
                raise ValueError("Un administrador solo puede asignar una entidad externa al convenio.")
        elif assigner_entity.getRole() == Rol.exEntity:
            if user_entity.getRole() != Rol.admin:
                raise ValueError("Una entidad externa solo puede asignar un administrador al convenio.")
        else:
            raise ValueError("No tienes permisos para asignar usuarios a convenios.")

        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        agreement_entity = self._model_to_entity(db_agreement)
        agreement_entity.assign_user_id(user_entity)

        updated_agreement = self.agreement_dao.update(db, agreement_entity)
        self._notify_external_assignment(db, user_id, agreement_id)
        return self._model_to_schema(updated_agreement)

    def assign_project_to_agreement(self, db: Session, agreement_id: int, project_id: int, assigner_id: int) -> AgreementResponse:
        # Asigna un proyecto a un convenio

        assigner = self._get_and_validate_user(db, assigner_id)
        self._validate_admin_permissions(assigner, "asignar proyectos a convenios")

        try:
            self.project_service.get_project_with_user(db, project_id)
        except ValueError:
            raise ValueError(f"El proyecto con ID {project_id} no existe")

        updated_agreement = self.agreement_dao.assign_project(db, agreement_id, project_id)
        if not updated_agreement:
            raise ValueError(f"No se encontró el convenio con ID {agreement_id}")

        return self._model_to_schema(updated_agreement)

    def delete_agreement(self, db: Session, agreement_id: int, deleter_id: int) -> bool:
        # Elimina un convenio

        deleter = self._get_and_validate_user(db, deleter_id)
        self._validate_admin_permissions(deleter, "eliminar convenios")

        return self.agreement_dao.delete(db, agreement_id)

    # =====================================================
    # MÉTODOS DE CONSULTA
    # =====================================================

    def get_agreement_by_id(self, db: Session, agreement_id: int) -> AgreementResponse:
        # Obtiene un convenio por ID
        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        return self._model_to_schema(db_agreement)

    def list_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        # Lista todos los convenios

        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar todos los convenios")

        db_agreements = self.agreement_dao.list(db)
        return [self._model_to_schema(agreement) for agreement in db_agreements]

    def list_pending_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        # Lista convenios pendientes de aprobación

        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar convenios pendientes")

        db_agreements = self.agreement_dao.get_by_status(db, AgreementStatus.PENDING)
        return [self._model_to_schema(agreement) for agreement in db_agreements]

    def list_user_agreements(self, db: Session, user_id: int, requester_id: int) -> List[AgreementResponse]:
        # Lista convenios de un usuario específico

        requester = self._get_and_validate_user(db, requester_id)
        if requester_id != user_id:
            self._validate_admin_permissions(requester, "listar convenios de otros usuarios")

        all_agreements = self.agreement_dao.list(db)
        user_agreements = [a for a in all_agreements if a.user_id == user_id]
        return [self._model_to_schema(a) for a in user_agreements]

    def get_project_for_agreement(self, db: Session, agreement_id: int, requester_id: int) -> Optional[ProyectComplete]:
        # Obtiene el proyecto asociado a un convenio

        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        if not db_agreement.project_id:
            return None

        try:
            return self.project_service.get_complete_project(db, db_agreement.project_id)
        except ValueError:
            return None

    def get_current_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        # Lista convenios vigentes (activos en la fecha actual)

        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar convenios vigentes")

        agreements = self.agreement_dao.list(db)
        return [self._model_to_schema(a) for a in agreements if a.is_current()]

    def get_expired_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        # Lista convenios expirados

        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar convenios expirados")

        agreements = self.agreement_dao.list(db)
        return [self._model_to_schema(a) for a in agreements if a.is_expired()]

    # =====================================================
    # MÉTODOS PRIVADOS - UTILIDADES Y VALIDACIONES
    # =====================================================

    def _get_and_validate_user(self, db: Session, user_id: int):
        try:
            return self.user_service.get_user_by_id(db, user_id)
        except ValueError:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")

    def _get_agreement_or_raise(self, db: Session, agreement_id: int) -> AgreementModel:
        agreement = self.agreement_dao.get_by_id(db, agreement_id)
        if not agreement:
            raise ValueError(f"Convenio con ID {agreement_id} no encontrado")
        return agreement

    def _validate_permissions(self, user) -> None:
        user_entity = self._user_to_entity(user)
        if user_entity.getRole() not in [Rol.admin, Rol.exEntity]:
            raise ValueError("No tienes permisos para crear convenios. Solo administradores y entidades externas pueden crear convenios.")

    def _validate_admin_permissions(self, user, action: str) -> None:
        if self._user_to_entity(user).getRole() != Rol.admin:
            raise ValueError(f"No tienes permisos para {action}. Solo administradores pueden realizar esta acción.")

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
            status=AgreementStatus(model.status),
            user_id=model.user_id,
            project_id=model.project_id
        )

    def _model_to_entity(self, model: AgreementModel) -> AgreementEntity:
        return AgreementEntity(
            id=model.id,
            start_date=model.start_date,
            end_date=model.end_date,
            user_id=model.user_id,
            project_id=model.project_id,
            status=AgreementStatus(model.status)
        )

    # =====================================================
    # MÉTODOS DE NOTIFICACIÓN
    # Las notificaciones no deberían interrumpir el flujo principal
    # =====================================================

    def _notify_agreement_creation(self, db: Session, user_id: int, agreement_id: int) -> None:
        try:
            NotificationService(db).notify(user_id, f"Se ha creado un nuevo convenio con ID {agreement_id} asociado a tu cuenta.")
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