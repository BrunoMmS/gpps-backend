from typing import List, Optional
from sqlalchemy.orm import Session
from cruds.agreementDAO import AgreementDAO
from entities.agreement_entity import AgreementEntity, AgreementStatus
from schemas.agreements_schema import AgreementCreate, AgreementUpdate, AgreementResponse, AgreementApproval
from schemas.project_schema import ProyectComplete
from models.agreement_model import AgreementModel
from services.user_service import UserService
from services.project_service import ProjectService
from services.rol import Rol
from services.notification_service import NotificationService


class AgreementService:
    
    def __init__(self):
        self.agreement_dao = AgreementDAO()
        self.user_service = UserService()
        self.project_service = ProjectService()
        self.notification_service = NotificationService()

    # =====================================================
    # MÉTODOS PÚBLICOS - OPERACIONES PRINCIPALES
    # =====================================================
    
    def create_agreement(self, db: Session, data: AgreementCreate, creator_id: int) -> AgreementResponse:
        #Crea un nuevo convenio.
        #Solo pueden crear convenios: Administradores y Entidades Externas
        
        creator = self._get_and_validate_user(db, creator_id)
        self._validate_creation_permissions(creator)
        
        # Crear entidad de convenio
        agreement_entity = AgreementEntity(
            start_date=data.start_date,
            end_date=data.end_date,
            external_entity_id=data.user_id,
            status=AgreementStatus.PENDING
        )
        
        # Si se proporciona user_id --> validar que sea entidad externa
        if data.user_id:
            external_user = self._get_and_validate_user(db, data.user_id)
            agreement_entity.assign_external_entity(self._user_to_entity(external_user))
        
        # Crear en BD
        db_agreement = self.agreement_dao.create(db, agreement_entity)
        
        # Notificar creación si es necesario
        if data.user_id and data.user_id != creator_id:
            self._notify_agreement_creation(db, data.user_id, db_agreement.id)
        
        return self._model_to_schema(db_agreement)
    
    def update_agreement(self, db: Session, agreement_id: int, data: AgreementUpdate, 
                        updater_id: int) -> AgreementResponse:
        
        #Actualiza un convenio existente
        
        updater = self._get_and_validate_user(db, updater_id)
        self._validate_admin_permissions(updater, "actualizar convenios")
        
        # Obtener convenio existente
        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        agreement_entity = self._model_to_entity(db_agreement)
        
        # Actualizar campos proporcionados
        if data.start_date and data.end_date:
            agreement_entity.update_dates(data.start_date, data.end_date)
        
        if data.status:
            agreement_entity.update_status(data.status)
        
        if data.user_id:
            external_user = self._get_and_validate_user(db, data.user_id)
            agreement_entity.assign_external_entity(self._user_to_entity(external_user))
        
        if data.project_id:
            # Validar que el proyecto existe
            try:
                self.project_service.get_project_with_user(db, data.project_id)
            except ValueError:
                raise ValueError(f"El proyecto con ID {data.project_id} no existe")
        
        # Actualizar en BD
        updated_agreement = self.agreement_dao.update(db, agreement_entity)
        return self._model_to_schema(updated_agreement)
    
    def approve_agreement(self, db: Session, agreement_id: int, 
                         approved_by_id: int) -> AgreementResponse:
        
        #Aprueba un convenio
        
        approver = self._get_and_validate_user(db, approved_by_id)
        approver_entity = self._user_to_entity(approver)
        
        # Obtener y aprobar convenio
        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        agreement_entity = self._model_to_entity(db_agreement)
        
        agreement_entity.approve(approver_entity)
        
        # Actualizar en BD
        updated_agreement = self.agreement_dao.update(db, agreement_entity)
        
        # Notificar aprobación
        if updated_agreement.user_id:
            self._notify_agreement_approval(db, updated_agreement.user_id, agreement_id)
        
        return self._model_to_schema(updated_agreement)
    
    def reject_agreement(self, db: Session, agreement_id: int, 
                        rejected_by_id: int) -> AgreementResponse:
        
        #Rechaza un convenio

        rejecter = self._get_and_validate_user(db, rejected_by_id)
        rejecter_entity = self._user_to_entity(rejecter)
        
        # Obtener y rechazar convenio
        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        agreement_entity = self._model_to_entity(db_agreement)
        
        agreement_entity.reject(rejecter_entity)
        
        # Actualizar en BD
        updated_agreement = self.agreement_dao.update(db, agreement_entity)
        
        # Notificar rechazo
        if updated_agreement.user_id:
            self._notify_agreement_rejection(db, updated_agreement.user_id, agreement_id)
        
        return self._model_to_schema(updated_agreement)
    
    def assign_external_representative(self, db: Session, agreement_id: int, 
                                     user_id: int, assigner_id: int) -> AgreementResponse:
        
        #Asigna una entidad externa al convenio
        
        # Validar permisos del asignador
        assigner = self._get_and_validate_user(db, assigner_id)
        self._validate_admin_permissions(assigner, "asignar representantes externos")
        
        # Validar que el usuario a asignar sea entidad externa
        external_user = self._get_and_validate_user(db, user_id)
        external_entity = self._user_to_entity(external_user)
        
        # Obtener convenio y asignar
        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        agreement_entity = self._model_to_entity(db_agreement)
        
        agreement_entity.assign_external_entity(external_entity)
        
        # Actualizar en BD
        updated_agreement = self.agreement_dao.update(db, agreement_entity)
        
        # Notificar asignación
        self._notify_external_assignment(db, user_id, agreement_id)
        
        return self._model_to_schema(updated_agreement)
    
    def assign_project_to_agreement(self, db: Session, agreement_id: int, 
                                  project_id: int, assigner_id: int) -> AgreementResponse:
        
        #Asigna un proyecto a un convenio
        
        # Validar permisos
        assigner = self._get_and_validate_user(db, assigner_id)
        self._validate_admin_permissions(assigner, "asignar proyectos a convenios")
        
        # Validar que el proyecto existe
        try:
            project = self.project_service.get_project_with_user(db, project_id)
        except ValueError:
            raise ValueError(f"El proyecto con ID {project_id} no existe")
        
        # Asignar proyecto al convenio
        updated_agreement = self.agreement_dao.assign_project(db, agreement_id, project_id)
        if not updated_agreement:
            raise ValueError(f"No se encontró el convenio con ID {agreement_id}")
        
        return self._model_to_schema(updated_agreement)
    
    def delete_agreement(self, db: Session, agreement_id: int, deleter_id: int) -> bool:
        
        #Elimina un convenio
        
        deleter = self._get_and_validate_user(db, deleter_id)
        self._validate_admin_permissions(deleter, "eliminar convenios")
        
        return self.agreement_dao.delete(db, agreement_id)
    
    # =====================================================
    # MÉTODOS DE CONSULTA
    # =====================================================
    
    def get_agreement_by_id(self, db: Session, agreement_id: int) -> AgreementResponse:
        #Obtiene un convenio por ID
        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        return self._model_to_schema(db_agreement)
    
    def list_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        
        #Lista todos los convenios
        
        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar todos los convenios")
        
        db_agreements = self.agreement_dao.list(db)
        return [self._model_to_schema(agreement) for agreement in db_agreements]
    
    def list_pending_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        
        #Lista convenios pendientes de aprobación
        
        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar convenios pendientes")
        
        db_agreements = self.agreement_dao.get_by_status(db, AgreementStatus.PENDING)
        return [self._model_to_schema(agreement) for agreement in db_agreements]
    
    def list_user_agreements(self, db: Session, user_id: int, 
                           requester_id: int) -> List[AgreementResponse]:
        
        #Lista convenios de un usuario específico
        
        requester = self._get_and_validate_user(db, requester_id)
        
        # Validar permisos: el usuario puede ver sus propios convenios o ser admin
        if requester_id != user_id:
            self._validate_admin_permissions(requester, "listar convenios de otros usuarios")
        
        # Filtrar convenios por usuario (esto requiere modificar el DAO)
        all_agreements = self.agreement_dao.list(db)
        user_agreements = [
            agreement for agreement in all_agreements 
            if agreement.user_id == user_id
        ]
        
        return [self._model_to_schema(agreement) for agreement in user_agreements]
    
    def get_project_for_agreement(self, db: Session, agreement_id: int, 
                                requester_id: int) -> Optional[ProyectComplete]:
        
        #Obtiene el proyecto asociado a un convenio
        
        # Validar que el convenio existe
        db_agreement = self._get_agreement_or_raise(db, agreement_id)
        
        if not db_agreement.project_id:
            return None
        
        try:
            return self.project_service.get_complete_project(db, db_agreement.project_id)
        except ValueError:
            return None
    
    def get_current_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        
        #Lista convenios vigentes (activos en la fecha actual)
        
        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar convenios vigentes")
        
        all_agreements = self.agreement_dao.list(db)
        current_agreements = [
            agreement for agreement in all_agreements 
            if agreement.is_current()
        ]
        
        return [self._model_to_schema(agreement) for agreement in current_agreements]
    
    def get_expired_agreements(self, db: Session, requester_id: int) -> List[AgreementResponse]:
        
        #Lista convenios expirados
        
        requester = self._get_and_validate_user(db, requester_id)
        self._validate_admin_permissions(requester, "listar convenios expirados")
        
        all_agreements = self.agreement_dao.list(db)
        expired_agreements = [
            agreement for agreement in all_agreements 
            if agreement.is_expired()
        ]
        
        return [self._model_to_schema(agreement) for agreement in expired_agreements]
    
    # =====================================================
    # MÉTODOS PRIVADOS - UTILIDADES Y VALIDACIONES
    # =====================================================
    
    def _get_and_validate_user(self, db: Session, user_id: int):
        #Obtiene un usuario y valida que existe
        try:
            return self.user_service.get_user_by_id(db, user_id)
        except ValueError:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")
    
    def _get_agreement_or_raise(self, db: Session, agreement_id: int) -> AgreementModel:
        #Obtiene un convenio o excepción si no existe
        db_agreement = self.agreement_dao.get_by_id(db, agreement_id)
        if not db_agreement:
            raise ValueError(f"Convenio con ID {agreement_id} no encontrado")
        return db_agreement
    
    def _validate_creation_permissions(self, user) -> None:
        #Valida que el usuario puede crear convenios
        user_entity = self._user_to_entity(user)
        allowed_roles = [Rol.admin, Rol.exEntity] #Roles permitido para crear un convenio
        
        if user_entity.getRole() not in allowed_roles:
            raise ValueError(
                "No tienes permisos para crear convenios. "
                "Solo administradores y entidades externas pueden crear convenios."
            )
    
    def _validate_admin_permissions(self, user, action: str) -> None:
        #Valida que el usuario sea administrador para realizar la acción
        user_entity = self._user_to_entity(user)
        
        if user_entity.getRole() != Rol.admin:
            raise ValueError(f"No tienes permisos para {action}. Solo administradores pueden realizar esta acción.")
    
    def _user_to_entity(self, user):
        #Convierte un esquema de usuario a entidad
        return self.user_service.to_entity(user)
    
    def _model_to_schema(self, model: AgreementModel) -> AgreementResponse:
        #Convierte un modelo de BD a schema de respuesta
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
        #Convierte un modelo de BD a entidad de convenio
        return AgreementEntity(
            id=model.id,
            start_date=model.start_date,
            end_date=model.end_date,
            external_entity_id=model.user_id,
            project_id=model.project_id,
            status=AgreementStatus(model.status)
        )
    
    # =====================================================
    # MÉTODOS DE NOTIFICACIÓN
    # Las notificaciones no deberían interrumpir el flujo principal
    # =====================================================
    
    def _notify_agreement_creation(self, db: Session, user_id: int, agreement_id: int) -> None:
        #Notifica la creación de un convenio
        try:
            notification_service = NotificationService(db)
            notification_service.notify(
                user_id, 
                f"Se ha creado un nuevo convenio con ID {agreement_id} asociado a tu cuenta."
            )
        except Exception:
            pass
    
    def _notify_agreement_approval(self, db: Session, user_id: int, agreement_id: int) -> None:
        #Notifica la aprobación de un convenio
        try:
            notification_service = NotificationService(db)
            notification_service.notify(
                user_id, 
                f"Tu convenio con ID {agreement_id} ha sido aprobado."
            )
        except Exception:
            pass
    
    def _notify_agreement_rejection(self, db: Session, user_id: int, agreement_id: int) -> None:
        #Notifica el rechazo de un convenio
        try:
            notification_service = NotificationService(db)
            notification_service.notify(
                user_id, 
                f"Tu convenio con ID {agreement_id} ha sido rechazado."
            )
        except Exception:
            pass
    
    def _notify_external_assignment(self, db: Session, user_id: int, agreement_id: int) -> None:
        #Notifica la asignación como representante externo
        try:
            notification_service = NotificationService(db)
            notification_service.notify(
                user_id, 
                f"Has sido asignado como representante externo del convenio con ID {agreement_id}."
            )
        except Exception:
            pass