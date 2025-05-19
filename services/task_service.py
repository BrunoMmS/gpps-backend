from sqlalchemy.orm import Session
from cruds.taskDAO import TaskDAO

class TaskService:
    def __init__(self):
        self.tasks_dao = TaskDAO()

    def set_done(self, db: Session, task_id: int) -> bool:
        task = self.tasks_dao.get_task(db, task_id)
        if task:
            task.done = True
            db.commit()
            return True
        return False
    
    def get_done(self, db: Session, task_id: int) -> bool:
        task = self.tasks_dao.get_task(db, task_id)
        return task.done if task else False