from sqlalchemy.orm import Session
from cruds.tasksDAO import tasksDAO
from models.tasks_model import Task

class tasksService:
    def __init__(self):
        self.tasks_dao = tasksDAO()
    
    def set_done(self, db: Session, task_id: int) -> bool:
        Task.done = True
        return True
    
    def get_done(self, db: Session, task_id: int) -> bool:
        task = self.tasks_dao.get_task(db, task_id)
        return task.done if task else False