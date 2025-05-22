from sqlalchemy.orm import Session
from cruds.taskDAO import TaskDAO
from schemas.task_schema import TaskCreate
class TaskService:
    def __init__(self):
        self.tasks_dao = TaskDAO()

    def set_done(self, db: Session, task_id: int) -> bool:
        task = self.tasks_dao.get_by_id(db, task_id)
        if task:
            task.done = True
            db.commit()
            return True
        return False
    
    def get_done(self, db: Session, task_id: int) -> bool:
        task = self.tasks_dao.get_by_id(db, task_id)
        return task.done if task else False
    
    def createTask(self, task_data: TaskCreate):
        new_task = self.tasks_dao.create(task_data)
        return new_task