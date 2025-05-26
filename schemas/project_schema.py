from datetime import date
from pydantic import BaseModel
from typing import Optional
from user_schema import User
from workplan_schema import WorkPlan

class ProjectWithUser(BaseModel):
    id: int
    title: str
    description: str
    active: bool
    start_date: date
    end_date: Optional[date] = None
    user: User

class ProjectComplete(BaseModel):
    id: int
    title: str
    description: str
    active: bool
    start_date: date
    end_date: Optional[date] = None
    user: User #schema
    workplan: WorkPlan #schema

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