from sqlalchemy.orm import Session
from models.task_model import TaskModel
from schema.task_schema import Task
from models.activity_model import ActivityModel

class TaskDAO:

    def get_by_id(self, db: Session, task_id: int) -> Task | None:
        return db.query(TaskModel).filter(TaskModel.id == task_id).first()

    def list_by_activity(self, db: Session, activity_id: int) -> list[TaskModel]:
        return db.query(TaskModel).filter(TaskModel.activity_id == activity_id).all()

    def create(self, db: Session, task_data: Task, activity_id: int) -> Task:
        db_task = TaskModel(**task_data.dict(), activity_id=activity_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def associate_task_to_activity(self, db: Session, task_id: int, activity_id: int) -> TaskModel:
        task = self.get_by_id(db, task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")
        activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
        if not activity:
            raise ValueError(f"Activity with id {activity_id} not found")
        task.activity_id = activity_id
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
