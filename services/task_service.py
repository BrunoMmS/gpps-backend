from sqlalchemy.orm import Session
from cruds.taskDAO import TaskDAO
from schemas.task_schema import TaskCreate
from models.task_model import TaskModel
from entities.task_entity import TaskEntity
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
    
    def task_to_entity(self, task_model: TaskModel) -> TaskEntity:
        if task_model is None:
            return None
        return TaskEntity(
            id=task_model.id,
            description=task_model.description,
            done=task_model.done
        )