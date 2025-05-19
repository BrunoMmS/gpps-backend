from datetime import date
from schema.workplan_schema import WorkPlan
from pydantic import BaseModel

class Project(BaseModel):
    id: int
    title: str
    description: str
    active: bool
    start_date: date
    end_date: date
    workplan: WorkPlan 

class ProjectCreate(Project):
    pass