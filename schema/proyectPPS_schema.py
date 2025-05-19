from datetime import datetime
from workplan_schema import work_plan
from pydantic import BaseModel
class proyect_PPS(BaseModel):
    title: str
    description: str
    active: bool
    start_date: datetime
    end_date: datetime
    workplan: work_plan
    id: int
    