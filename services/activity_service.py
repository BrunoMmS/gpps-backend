from sqlalchemy.orm import Session
from cruds.taskDAO import TaskDAO
from cruds.activityDAO import ActivityDAO
from cruds.workplanDAO import WorkPlanDAO
from schemas.activity_schema import ActivitieCreate
from schemas.task_schema import TaskCreate
from models.activity_model import ActivityModel
from models.task_model import TaskModel

class ActivityService:
    def __init__(self):
        self.activity_dao = ActivityDAO()
        self.workplan_dao = WorkPlanDAO()
        self.tasks_dao = TaskDAO()

    def is_complete(self, db: Session, activity_id: int) -> bool:
        activity = self.activity_dao.get_by_id(db, activity_id)
        if not activity:
            return False
        
        tasks = self.tasks_dao.list_by_activity(db, activity_id)
        return all(task.done for task in tasks)

    def create_activity(self, db: Session, workplan_id: int, activity_data: ActivitieCreate) -> ActivityModel:
        workplan = self.workplan_dao.get_by_id(db, workplan_id)
        if not workplan:
            raise ValueError("Plan de trabajo no encontrado")

        new_activity = self.activity_dao.create(db, activity_data, workplan_id)
        return new_activity

    def append_task(self, db: Session, activity_id: int, new_task_data: TaskCreate) -> TaskModel:
        activity = self.activity_dao.get_by_id(db, activity_id)
        if not activity:
            raise ValueError("Actividad no encontrada")

        task = self.tasks_dao.create(db, new_task_data, activity_id)
        return task
    
    def get_activities_by_workplan(self, db: Session, workplan_id: int):
        return self.activity_dao.list_by_workplan(db, workplan_id)