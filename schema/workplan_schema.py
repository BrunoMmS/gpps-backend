from pydantic import BaseModel
from schema.activity_schema import Activitie

class WorkPlan(BaseModel):
    id: int
    description: str
    activities: list[Activitie]

class WorkPlanCreate(BaseModel):
    description: str