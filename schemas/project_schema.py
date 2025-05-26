from datetime import date
from pydantic import BaseModel
from typing import Optional
from schemas.workplan_schema import WorkPlan
class Project(BaseModel):
    id: int
    title: str
    description: str
    active: bool
    start_date: date
    user_id: int
    end_date: Optional[date] = None
#   tutor_id: Optional[int] = None

class ProjectCreate(BaseModel):
    title: str
    description: str
    active: bool
    start_date: date
    user_id: int
    end_date: Optional[date] = None

class ProyectComplete(BaseModel):
    id: int
    title: str
    description: str
    active: bool
    start_date: date
    user_id: int
    end_date: Optional[date] = None
    workplan: Optional[WorkPlan] = None

    class Config:
        from_attributes = True

"""
class ProjectWithCreator(BaseModel):
    id: int
    name: str
    description: str
    active: bool
    tutor_id: Optional[int] = None
    user_id: int
    creator: User  # Información completa del usuario creador
"""