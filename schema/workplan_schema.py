from pydantic import BaseModel
from schema.activity_schema import Activity

class WorkPlan(BaseModel):
    id: int
    description: str
    activities: list[Activity]

class WorkPlanCreate(BaseModel):
    description: str
    activities: list[Activity]