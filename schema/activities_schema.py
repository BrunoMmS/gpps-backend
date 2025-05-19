from pydantic import BaseModel
from schema.tasks_schema import Task

class Activitie(BaseModel):
    name: str
    duration: int
    id: int
    done: bool
    jobs: list[Task]