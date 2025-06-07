from sqlalchemy.orm import Session
from models.agreement_model import AgreementModel
from entities.agreement_entity import AgreementEntity, AgreementStatus
from typing import List, Optional

class AgreementDAO:
    def get_by_id(self, db: Session, agreement_id: int) -> Optional[AgreementModel]:
        """Obtiene un convenio por ID"""
        try:
            return db.query(AgreementModel).filter(AgreementModel.id == agreement_id).first()
        except Exception as e:
            raise ValueError(f"No se pudo obtener el convenio con ID {agreement_id}: {e}")

    def list(self, db: Session) -> List[AgreementModel]:
        """Lista todos los convenios"""
        try:
            return db.query(AgreementModel).all()
        except Exception as e:
            raise ValueError(f"No se pudieron listar los convenios: {e}")

    def create(self, db: Session, agreement_entity: AgreementEntity) -> AgreementModel:
        #Crea un nuevo convenio
        try:
            agreement = AgreementModel(
                start_date=agreement_entity.get_start_date(),
                end_date=agreement_entity.get_end_date(),
                current=agreement_entity.is_current(),
                status=agreement_entity.get_status().value,
                user_id=agreement_entity.get_user_id(),  # Puede ser None
            )
            db.add(agreement)
            db.commit()
            db.refresh(agreement)
            return agreement
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo crear el convenio: {e}")

    def update(self, db: Session, agreement_entity: AgreementEntity) -> AgreementModel:
        """Actualiza un convenio existente"""
        try:
            agreement = db.query(AgreementModel).filter(
                AgreementModel.id == agreement_entity.get_id()
            ).first()
            
            if not agreement:
                raise ValueError(f"No se encontró el convenio con ID {agreement_entity.get_id()}")

            agreement.start_date = agreement_entity.get_start_date()
            agreement.end_date = agreement_entity.get_end_date()
            agreement.current = agreement_entity.is_current()
            agreement.status = agreement_entity.get_status().value
            agreement.user_id = agreement_entity.get_user_id()
            
            db.commit()
            db.refresh(agreement)
            return agreement
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo actualizar el convenio con ID {agreement_entity.get_id()}: {e}")
    
    def delete(self, db: Session, agreement_id: int) -> bool:
        """Elimina un convenio"""
        try:
            agreement = self.get_by_id(db, agreement_id)
            if not agreement:
                return False
            
            db.delete(agreement)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo eliminar el convenio con ID {agreement_id}: {e}")
    
    def get_by_status(self, db: Session, status: AgreementStatus) -> List[AgreementModel]:
        """Obtiene convenios por estado"""
        try:
            return db.query(AgreementModel).filter(AgreementModel.status == status.value).all()
        except Exception as e:
            raise ValueError(f"No se pudieron obtener convenios con estado '{status.name}': {e}")
    
    def get_current_agreements(self, db: Session) -> List[AgreementModel]:
        """Obtiene convenios vigentes"""
        try:
            return db.query(AgreementModel).filter(AgreementModel.current == True).all()
        except Exception as e:
            raise ValueError(f"No se pudieron obtener los convenios vigentes: {e}")
            
    def get_by_external_entity(self, db: Session, entity_id: int) -> List[AgreementModel]:
        """Obtiene convenios por entidad externa"""
        try:
            return db.query(AgreementModel).filter(AgreementModel.user_id == entity_id).all()
        except Exception as e:
            raise ValueError(f"No se pudieron obtener convenios de la entidad externa con ID {entity_id}: {e}")
    
    def deactivate(self, db: Session, agreement_id: int) -> bool:
        """Desactiva un convenio"""
        try:
            agreement = self.get_by_id(db, agreement_id)
            if not agreement:
                return False
            
            agreement.current = False
            agreement.status = AgreementStatus.INACTIVE.value
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo desactivar el convenio con ID {agreement_id}: {e}")
    
    def assign_external_representative(self, db: Session, agreement_id: int, user_id: int) -> AgreementModel:
        """Asigna un representante externo al convenio"""
        try:
            agreement = self.get_by_id(db, agreement_id)
            if not agreement:
                raise ValueError(f"No se encontró el convenio con ID {agreement_id}")
            
            agreement.user_id = user_id
            db.commit()
            db.refresh(agreement)
            return agreement
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo asignar el representante externo con ID {user_id} al convenio {agreement_id}: {e}")
    
    def get_projects(self, db: Session, agreement_id: int) -> List:
        """Obtiene proyectos asociados a un convenio"""
        try:
            from models.project_model import ProjectModel
            return db.query(ProjectModel).filter(ProjectModel.agreement_id == agreement_id).all()
        except Exception as e:
            raise ValueError(f"No se pudieron obtener los proyectos del convenio con ID {agreement_id}: {e}")