from sqlalchemy.orm import Session
from models.task_model import TaskTable
from schema.task_schema import Task

# Esta clase fue modicada para que el nombre de la tabla sea TaskTable - Joaco

class TaskDAO:

    def get_by_id(self, db: Session, task_id: int) -> Task | None:
        return db.query(TaskTable).filter(TaskTable.id == task_id).first()

    def list_by_activity(self, db: Session, activity_id: int) -> list[Task]:
        return db.query(TaskTable).filter(TaskTable.activity_id == activity_id).all()

    def create(self, db: Session, task_data: Task) -> Task:
        db_task = TaskTable(**task_data.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task