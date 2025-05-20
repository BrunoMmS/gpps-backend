from sqlalchemy.orm import Session
from cruds.workplanDAO import WorkPlanDAO
from schema.workplan_schema import WorkPlanCreate
class WorkPlanService:
    def __init__(self):
        self.workplan_dao = WorkPlanDAO()

    def create_workplan(self, db: Session,  workplan_data: WorkPlanCreate) -> WorkPlanCreate:

        return self.workplan_dao.create(db, workplan_data)
    
    