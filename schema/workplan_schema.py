from pydantic import BaseModel
from activities_schema import activities
class work_plan(BaseModel):
    activities=[activities]
    id : int