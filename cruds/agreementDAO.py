from sqlalchemy.orm import Session
from models.agreement_model import AgreementModel
from entities.agreement_entity import AgreementEntity, AgreementStatus
from typing import List, Optional

class AgreementDAO:

    def create(self, db: Session, agreement_entity: AgreementEntity) -> AgreementModel:
        """Crea un nuevo convenio"""
        try:
            db_agreement = AgreementModel(
                start_date=agreement_entity.get_start_date,
                end_date=agreement_entity.get_end_date,
                status=agreement_entity.get_status.value,
                user_id=agreement_entity.get_external_entity_id,
                project_id=agreement_entity.get_project_id
            )
            db.add(db_agreement)
            db.commit()
            db.refresh(db_agreement)
            return db_agreement
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo crear el convenio: {e}")

    def update(self, db: Session, agreement_entity: AgreementEntity) -> AgreementModel:
        """Actualiza un convenio existente"""
        try:
            agreement = db.query(AgreementModel).filter(AgreementModel.id == agreement_entity.get_id).first()
            if not agreement:
                raise ValueError(f"No se encontró el convenio con ID {agreement_entity.get_id}")

            agreement.start_date = agreement_entity.get_start_date
            agreement.end_date = agreement_entity.get_end_date
            agreement.status = agreement_entity.get_status.value
            agreement.user_id = agreement_entity.get_external_entity_id
            agreement.project_id = agreement_entity.get_project_id

            db.commit()
            db.refresh(agreement)
            return agreement
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo actualizar el convenio con ID {agreement_entity.get_id}: {e}")

    def update_status(self, db: Session, agreement_id: int, new_status: str) -> AgreementModel | None:
        agreement = self.get_by_id(db, agreement_id)
        if not agreement:
            return None
        agreement.status = new_status
        db.commit()
        db.refresh(agreement)
        return agreement
    
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
        
    def get_by_status(self, db: Session, status: AgreementStatus) -> List[AgreementModel]:
        """Obtiene convenios por estado"""
        try:
            return db.query(AgreementModel).filter(AgreementModel.status == status.value).all()
        except Exception as e:
            raise ValueError(f"No se pudieron obtener convenios con estado '{status.name}': {e}")

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

    def assign_project(self, db: Session, agreement_id: int, project_id: int) -> AgreementModel:
        """Asigna un proyecto al convenio"""
        try:
            agreement = self.get_by_id(db, agreement_id)
            if not agreement:
                raise ValueError(f"No se encontró el convenio con ID {agreement_id}")
            agreement.project_id = project_id
            db.commit()
            db.refresh(agreement)
            return agreement
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo asignar el proyecto con ID {project_id} al convenio {agreement_id}: {e}")