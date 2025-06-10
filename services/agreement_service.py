from typing import List, Optional
from sqlalchemy.orm import Session
from cruds.agreementDAO import AgreementDAO
from entities.agreement_entity import AgreementEntity, AgreementStatus
from entities.user_entity import UserEntity
from schemas.agreements_schema import AgreementCreate, AgreementUpdate, Agreement
from models.agreement_model import AgreementModel
from models.project_model import ProjectModel
from schemas.project_schema import Project
from services.user_service import UserService
from services.project_service import ProjectService
from schemas.project_schema import ProyectComplete

class AgreementService:
    def __init__(self):
        self.dao = AgreementDAO()
        self.user_service = UserService()
        self.proyect_service= ProjectService()

        
    def create_agreement(self, db: Session, data: AgreementCreate) -> AgreementModel:
        """Crea un nuevo convenio"""
        try:
            agreement_entity = AgreementEntity(
                id=None,
                start_date=data.start_date,
                end_date=data.end_date,
                external_entity= self.user_service.to_entity(self.user_service.get_user_by_id(db, data.user_id))
            )
            created_model = self.dao.create(db, agreement_entity)
            return self._model_to_schema(created_model)
        except Exception as e:
            raise ValueError(f"Error creating agreement: {e}")
        

    def update_agreement(self, db: Session, agreement_id: int, data: AgreementUpdate) -> AgreementModel:
        """Actualiza un convenio existente"""
        try:
            existing_model = self.dao.get_by_id(db, agreement_id)
            if not existing_model:
                raise ValueError(f"Convenio con ID {agreement_id} no encontrado")
            
            agreement_entity = self._model_to_entity(existing_model)
            
            if data.start_date is not None and data.end_date is not None:
                agreement_entity.update_dates(data.start_date, data.end_date)
            
            if data.status is not None:
                agreement_entity.update_status(AgreementStatus(data.status))
            
            if data.user_id is not None:
                agreement_entity._external_entity = UserEntity(id=data.user_id)
                
            if data.project is not None:
                agreement_entity._project = data.project   
            
            updated_model = self.dao.update(db, agreement_entity)
            return self._model_to_schema(updated_model)
        except Exception as e:
            raise ValueError(f"Error updating agreement {agreement_id}: {e}")

    def get_agreement_by_id(self, db: Session, agreement_id: int) -> Agreement:
        """Obtiene un convenio por ID"""
        try:
            model = self.dao.get_by_id(db, agreement_id)
            if not model:
                raise ValueError(f"Convenio con ID {agreement_id} no encontrado")
            return self._model_to_schema(model)
        except Exception as e:
            raise ValueError(f"Error getting agreement {agreement_id}: {e}")

    def list_agreements(self, db: Session) -> List[Agreement]:
        """Lista todos los convenios"""
        try:
            models = self.dao.list(db)
            return [self._model_to_schema(model) for model in models]
        except Exception as e:
            raise ValueError(f"Error listing agreements: {e}")

    def list_pending_agreements(self, db: Session) -> List[Agreement]:
        """Lista convenios pendientes de aprobación"""
        try:
            models = self.dao.get_by_status(db, AgreementStatus.PENDING)
            return [self._model_to_schema(model) for model in models]
        except Exception as e:
            raise ValueError(f"Error listing pending agreements: {e}")
    
    def delete_agreement(self, db: Session, agreement_id: int) -> bool:
        """Elimina un convenio"""
        try:
            result = self.dao.delete(db, agreement_id)
            if not result:
                raise ValueError(f"No se pudo eliminar el convenio con ID {agreement_id}")
            return result
        except Exception as e:
            raise ValueError(f"Error deleting agreement {agreement_id}: {e}")
    
    def deactivate_agreement(self, db: Session, agreement_id: int) -> bool:
        """Desactiva un convenio"""
        try:
            agreement = self.dao.get_by_id(db, agreement_id)
            if not agreement:
                raise ValueError(f"Convenio con ID {agreement_id} no encontrado")
            
            result = self.dao.deactivate(db, agreement_id)
            if not result:
                raise ValueError(f"No se pudo desactivar el convenio con ID {agreement_id}")
            return result
        except Exception as e:
            raise ValueError(f"Error deactivating agreement {agreement_id}: {e}")

    def approve_agreement(self, db: Session, agreement_id: int, approved_by_id: Optional[int] = None) -> Agreement:
        """Aprueba un convenio"""
        try:
            user= self.user_service.get_user_by_id(approved_by_id)
            if not user:
                raise ValueError(f"El usuario no existe y por lo tanto no se puede aprobar el convenio")
            
            user_entity= self.user_service.to_entity(user)
            if user_entity.getRole != "Administrator":
                raise ValueError(f"El usuario no tiene los permisos para aprobar el convenio")
            
            existing_model = self.dao.get_by_id(db, agreement_id)
            if not existing_model:
                raise ValueError(f"Convenio con ID {agreement_id} no encontrado")
            agreement_entity = self._model_to_entity(existing_model)
            
            if agreement_entity.get_status() != AgreementStatus.PENDING:
                raise ValueError("Solo se pueden aprobar convenios pendientes")
            
            agreement_entity.update_status(AgreementStatus.APPROVED)
            
            updated_model = self.dao.update(db, agreement_entity)
            return self._model_to_schema(updated_model)
        except Exception as e:
            raise ValueError(f"Error approving agreement {agreement_id}: {e}")
    
    def reject_agreement(self, db: Session, agreement_id: int, rejected_by_id: Optional[int] = None) -> Agreement:
        """Rechaza un convenio"""
        try:
            user= self.user_service.get_user_by_id(rejected_by_id)
            if not user:
                raise ValueError(f"El usuario no existe y por lo tanto no se puede rechazar el convenio")
            user_entity= self.user_service.to_entity(user)
        
            if user_entity.getRole != "Administrator":
                raise ValueError(f"El usuario no tiene los permisos para aprobar el convenio")
            
            existing_model = self.dao.get_by_id(db, agreement_id)
            if not existing_model:
                raise ValueError(f"Convenio con ID {agreement_id} no encontrado")
            agreement_entity = self._model_to_entity(existing_model)
            
            if agreement_entity.get_status() != AgreementStatus.PENDING:
                raise ValueError("Solo se pueden rechazar convenios pendientes")
            
            agreement_entity.update_status(AgreementStatus.REJECTED)
            
            updated_model = self.dao.update(db, agreement_entity)
            return self._model_to_schema(updated_model)
        except Exception as e:
            raise ValueError(f"Error rejecting agreement {agreement_id}: {e}")
    
    def assign_external_representative(self, db: Session, agreement_id: int, user_id: int) -> Agreement:
        """Asigna un representante externo al convenio"""
        try:
            agreement = self.dao.get_by_id(db, agreement_id)
            if not agreement:
                raise ValueError(f"Convenio con ID {agreement_id} no encontrado")

            updated = self.dao.assign_external_representative(db, agreement_id, user_id)
            return self._model_to_schema(updated)
        except Exception as e:
            raise ValueError(f"Error assigning external representative: {e}")

    def get_project_for_agreement(self, db: Session, agreement_id: int) -> ProyectComplete:
        """Obtiene proyectos asociados a un convenio"""
        try:
            agreement = self.dao.get_by_id(db, agreement_id)
            project_complete= self.proyect_service.get_complete_project(db,agreement.project_id)
            return project_complete
        except Exception as e:
            raise ValueError(f"Error getting projects for agreement {agreement_id}: {e}")
    
    def _model_to_schema(self, model: AgreementModel) -> Agreement:
        """Convierte un modelo de BD a schema"""
        return Agreement(
            id=model.id,
            start_date=model.start_date,
            end_date=model.end_date,
            status=model.status,
            external_entity=None,  # Se puede expandir para incluir datos del usuario
            project=None  # Se puede expandir para incluir datos del proyecto
        )
        
    def _model_to_entity(self, model: AgreementModel) -> AgreementEntity:
        """Convierte un modelo de BD a entidad de dominio"""
        entity = AgreementEntity(
            id=model.id,
            start_date=model.start_date,
            end_date=model.end_date,
            status=AgreementStatus(model.status)
        )
        return entity