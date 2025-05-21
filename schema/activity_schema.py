from typing import Optional
from pydantic import BaseModel
from schema.task_schema import Task, TaskCreate
class Activitie(BaseModel):
    id: int
    name: str
    duration: int
    done: bool
    jobs: Optional[list[Task]] = []
    class Config:
        from_attributes = True

class ActivitieCreate(BaseModel):
    name: str
    duration: int
    done: bool