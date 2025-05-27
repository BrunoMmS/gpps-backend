from typing import Optional
from pydantic import BaseModel
from schemas.task_schema import Task, TaskCreate

class Activitie(BaseModel):
    id: int
    name: str
    duration: int
    done: bool
    tasks: Optional[list[Task]] = []
    class Config:
        from_attributes = True

class ActivitieCreate(BaseModel):
    name: str
    duration: int
    done: bool