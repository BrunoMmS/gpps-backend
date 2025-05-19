from sqlalchemy.orm import Session
from models.proyectPPS_model import ProyectPPS
from schema.proyectPPS_schema import ProyectCreate

class ProyectDAO:
    def get_by_id(self, db: Session, proyect_id: int) -> ProyectPPS | None:
        return db.query(ProyectPPS).filter(ProyectPPS.id == proyect_id).first()

    def list(self, db: Session) -> list[ProyectPPS]:
        return db.query(ProyectPPS).all()

    def create(self, db: Session, proyect_data: ProyectCreate) -> ProyectPPS:
        db_proyect = ProyectPPS(**proyect_data.dict())
        db.add(db_proyect)
        db.commit()
        db.refresh(db_proyect)
        return db_proyect