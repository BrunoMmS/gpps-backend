from sqlalchemy.orm import Session
from cruds.workplanDAO import WorkPlanDAO
from cruds.activityDAO import ActivityDAO
from cruds.taskDAO import TaskDAO
from schema.workplan_schema import WorkPlanCreate
class WorkPlanService:
    def __init__(self):
        self.activity_dao = ActivityDAO()
        self.workplan_dao = WorkPlanDAO()
        self.tasks_dao = TaskDAO()
    #def createWorkPlan(self, newWorkplan: WorkPlanCreate):

