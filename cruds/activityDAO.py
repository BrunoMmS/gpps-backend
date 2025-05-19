from sqlalchemy.orm import Session
from models.activity_model import ActivityModel
from schema.activity_schema import ActivityCreate

class ActivityDAO:
    def get_by_id(self, db: Session, activity_id: int) -> ActivityModel | None:
        return db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()

    def list_by_workplan(self, db: Session, workplan_id: int) -> list[ActivityModel]:
        return db.query(ActivityModel).filter(ActivityModel.workplan_id == workplan_id).all()

    def create(self, db: Session, activity_data: ActivityCreate) -> ActivityModel:
        db_activity = ActivityModel(**activity_data.dict())
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity