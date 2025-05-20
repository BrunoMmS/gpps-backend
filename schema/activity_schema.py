from pydantic import BaseModel
from schema.task_schema import Task, TaskCreate
class Activitie(BaseModel):
    id: int
    name: str
    duration: int
    done: bool
    jobs: list[Task]

class ActivitieCreate(BaseModel):
    name: str
    duration: int
    done: bool