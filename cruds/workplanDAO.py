from sqlalchemy.orm import Session
from models.workplan_model import WorkPlan
from schema.workplan_schema import WorkPlanCreate

class WorkPlanDAO:
    def get_by_id(self, db: Session, workplan_id: int) -> WorkPlan | None:
        return db.query(WorkPlan).filter(WorkPlan.id == workplan_id).first()

    def create(self, db: Session, workplan_data: WorkPlanCreate) -> WorkPlan:
        db_workplan = WorkPlan(**workplan_data.model_dump())
        db.add(db_workplan)
        db.commit()
        db.refresh(db_workplan)
        return db_workplan
    