from pydantic import BaseModel
from schema.activity_schema import Activitie
from typing import Optional

class WorkPlan(BaseModel):
    id: int
    project_id: int
    description: str
    activities: Optional[list[Activitie]] = None

class WorkPlanCreate(BaseModel):
    project_id: int
    description: str