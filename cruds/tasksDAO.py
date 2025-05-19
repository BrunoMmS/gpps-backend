from sqlalchemy.orm import Session
from models.tasks_model import Task
from schema.tasks_schema import tasks


class tasksDAO :
    
    
    def get_by_id(self, db: Session, task_id: int) -> tasks | None:
        return db.query(tasks).filter(tasks.id == task_id).first()
    
    def list_by_activity(self, db: Session, activity_id: int) -> list[tasks]:  
        return db.query(tasks).filter(tasks.activity_id == activity_id).all()
    
    def create(self, db: Session, task_data: tasks) -> tasks:
        db_task = tasks(**task_data.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task