from sqlalchemy.orm import Session
from cruds.tasksDAO import tasksDAO
from cruds.activitiesDAO import ActivitiesDAO
from cruds.workplanDAO import WorkPlanDAO

class activitiesService:
    def __init__(self):
        self.activities_dao = ActivitiesDAO()
        self.workplan_dao = WorkPlanDAO()
        self.tasks_dao = tasksDAO()

    def is_complete(self, db: Session, activity_id: int) -> bool:
        activity = self.activities_dao.get_by_id(db, activity_id)
        if not activity:
            return False
        tasks = self.tasks_dao.list_by_activity(db, activity_id)
        for task in tasks:
            if not task.done:
                return False
        self.done = True
        return True
    
    def get_complete_percentage(self, db: Session, activity_id: int) -> float:
        activity = self.activities_dao.get_by_id(db, activity_id)
        if not activity:
            return 0.0
        tasks = self.tasks_dao.list_by_activity(db, activity_id)
        total_tasks = len(tasks)
        if total_tasks == 0:
            return 0.0
        completed_tasks = sum(1 for task in tasks if task.done)
        return (completed_tasks / total_tasks) * 100
    
    def get_incomplete_percentage(self, db: Session, activity_id: int) -> float:
        activity = self.activities_dao.get_by_id(db, activity_id)
        if not activity:
            return 0.0
        tasks = self.tasks_dao.list_by_activity(db, activity_id)
        total_tasks = len(tasks)
        if total_tasks == 0:
            return 0.0
        incomplete_tasks = sum(1 for task in tasks if task.done == False)
        return (incomplete_tasks / total_tasks) * 100