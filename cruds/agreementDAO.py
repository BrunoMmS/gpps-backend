from sqlalchemy.orm import Session
from models.agreement_model import AgreementModel
from entities.agreement_entity import AgreementEntity, AgreementStatus
from typing import List, Optional

class AgreementDAO:

    def create(self, db: Session, entity: AgreementEntity) -> AgreementModel:
        #Crea un nuevo convenio desde una entidad de dominio
        try:
            model = AgreementModel(
                start_date=entity.get_start_date,
                end_date=entity.get_end_date,
                created_by=entity.get_created_by,
                user_id=entity.get_user_id,
                project_id=entity.get_project_id,
                status=entity.get_status.value
            )
            db.add(model)
            db.commit()
            db.refresh(model)
            return model
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo crear el convenio: {e}")

    def update(self, db: Session, entity: AgreementEntity) -> AgreementModel:
        #Actualiza un convenio existente a partir de una entidad
        try:
            model = self.get_by_id(db, entity.get_id)
            if not model:
                raise ValueError(f"No se encontró el convenio con ID {entity.get_id}")

            model.start_date = entity.get_start_date
            model.end_date = entity.get_end_date
            model.user_id = entity.get_user_id
            model.project_id = entity.get_project_id
            model.status = entity.get_status.value

            db.commit()
            db.refresh(model)
            return model
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo actualizar el convenio con ID {entity.get_id}: {e}")

    def delete(self, db: Session, agreement_id: int) -> bool:
        #Elimina un convenio por ID
        try:
            model = self.get_by_id(db, agreement_id)
            if not model:
                return False
            db.delete(model)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo eliminar el convenio con ID {agreement_id}: {e}")

    def get_by_id(self, db: Session, agreement_id: int) -> Optional[AgreementModel]:
        #Busca un convenio por ID
        return db.query(AgreementModel).filter_by(id=agreement_id).first()

    def list(self, db: Session) -> List[AgreementModel]:
        #Lista todos los convenios
        return db.query(AgreementModel).all()

    def get_by_status(self, db: Session, status: AgreementStatus) -> List[AgreementModel]:
        #Lista convenios por estado
        return db.query(AgreementModel).filter_by(status=status.value).all()

    def assign_external_representative(self, db: Session, agreement_id: int, user_id: int) -> AgreementModel:
        #Asigna un usuario externo a un convenio
        try:
            model = self.get_by_id(db, agreement_id)
            if not model:
                raise ValueError(f"No se encontró el convenio con ID {agreement_id}")
            model.user_id = user_id
            db.commit()
            db.refresh(model)
            return model
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo asignar el usuario {user_id} al convenio {agreement_id}: {e}")

    def assign_project(self, db: Session, agreement_id: int, project_id: int) -> AgreementModel:
        #Asigna un proyecto a un convenio
        try:
            model = self.get_by_id(db, agreement_id)
            if not model:
                raise ValueError(f"No se encontró el convenio con ID {agreement_id}")
            model.project_id = project_id
            db.commit()
            db.refresh(model)
            return model
        except Exception as e:
            db.rollback()
            raise ValueError(f"No se pudo asignar el proyecto {project_id} al convenio {agreement_id}: {e}")