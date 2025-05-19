from sqlalchemy.orm import Session
from models.activities_model import Activities
from schema.activities_schema import ActivitiesCreate

class ActivitiesDAO:
    def get_by_id(self, db: Session, activity_id: int) -> Activities | None:
        return db.query(Activities).filter(Activities.id == activity_id).first()

    def list_by_workplan(self, db: Session, workplan_id: int) -> list[Activities]:
        return db.query(Activities).filter(Activities.workplan_id == workplan_id).all()

    def create(self, db: Session, activity_data: ActivitiesCreate) -> Activities:
        db_activity = Activities(**activity_data.dict())
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity
