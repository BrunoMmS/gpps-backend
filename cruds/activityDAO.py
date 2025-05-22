from sqlalchemy.orm import Session
from models.activity_model import ActivityModel
from models.workplan_model import WorkPlan
from schemas.activity_schema import ActivitieCreate

class ActivityDAO:
    def get_by_id(self, db: Session, activity_id: int) -> ActivityModel | None:
        return db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()

    def list_by_workplan(self, db: Session, workplan_id: int) -> list[ActivityModel]:
        return db.query(ActivityModel).filter(ActivityModel.workplan_id == workplan_id).all()

    def create(self, db: Session, activity_data: ActivitieCreate, workplan_id: int) -> ActivityModel:
        db_activity = ActivityModel(**activity_data.dict(), workplan_id=workplan_id)
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity

    def associate_activity_to_workplan(self, db: Session, activity_id: int, workplan_id: int) -> ActivityModel:
        activity = self.get_by_id(db, activity_id)
        if not activity:
            raise ValueError(f"Activity with id {activity_id} not found")

        workplan = db.query(WorkPlan).filter(WorkPlan.id == workplan_id).first()
        if not workplan:
            raise ValueError(f"WorkPlan with id {workplan_id} not found")

        activity.workplan_id = workplan_id 

        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity