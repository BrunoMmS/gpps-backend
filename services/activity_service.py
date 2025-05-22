from sqlalchemy.orm import Session
from cruds.taskDAO import TaskDAO
from cruds.activityDAO import ActivityDAO
from cruds.workplanDAO import WorkPlanDAO
from schema.activity_schema import ActivitieCreate
from schema.task_schema import TaskCreate
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
        for task in tasks:
            if not task.done:
                return False
        self.done = True
        return True

    
    def create_Activities(self, newActivities: ActivitieCreate):
        new_activities= self.activity_dao.create(newActivities)
        return new_activities
    
    def append_Task(self,db: Session, activity_id: int, newTask: TaskCreate):
        activity = self.activity_dao.get_by_id(db, activity_id)
        if not activity:
            raise ValueError(f"Activity with id {activity_id} not found")
        task = self.tasks_dao.create(db, newTask)
        return task

    #mandar notificacion al completar una actividad o al mandar informes 

