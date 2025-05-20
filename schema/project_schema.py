from datetime import date
from schema.workplan_schema import WorkPlan
from pydantic import BaseModel
from typing import Optional

class Project(BaseModel):
    id: int
    title: str
    description: str
    active: bool
    tutor_id: int
    start_date: date
    end_date: date
    workplan: Optional[WorkPlan] = None

class ProjectCreate(BaseModel):
    title: str
    description: str
    active: bool
    start_date: date
    end_date: date