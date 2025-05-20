from sqlalchemy.orm import Session
from models.activity_model import ActivityModel
from schema.activity_schema import ActivitieCreate
from models.workplan_model import WorkPlan

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
    def associate_activity_to_workplan(self, db: Session, activity_id: int, workplan_id: int) -> ActivityModel:
        activity= self.get_by_id(db,activity_id)
        if not activity:
            raise ValueError(f"Task with id {activity_id} not found")
        workplan = db.query(WorkPlan).filter(WorkPlan.id == workplan_id).first()
        if not activity:
            raise ValueError(f"Activity with id {workplan_id} not found")
        #activity.workplan_id = workplan_id 
        #por alguna razon no deja guardar en activity el workplan_id, esto es lo q dejaria q se asocie a workplan
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity