from sqlalchemy.orm import Session
from models.activity_model import ActivityModel
from schema.activity_schema import ActivitieCreate

class ActivityDAO:
    def get_by_id(self, db: Session, activity_id: int) -> ActivitieCreate | None:
        return db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()

    def list_by_workplan(self, db: Session, workplan_id: int) -> list[ActivitieCreate]:
        return db.query(ActivityModel).filter(ActivityModel.workplan_id == workplan_id).all()

    def create(self, db: Session, activity_data: ActivitieCreate) -> ActivitieCreate:
        db_activity = ActivityModel(**activity_data.dict())
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity