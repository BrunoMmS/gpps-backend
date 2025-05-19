from datetime import date
from workplan_schema import work_plan
from pydantic import BaseModel

class Project(BaseModel):
    title: str
    description: str
    active: bool
    start_date: date
    end_date: date
    workplan: work_plan
    id: int
    