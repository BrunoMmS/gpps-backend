from pydantic import BaseModel
from schemas.user_schema import User 
from schemas.project_schema import ProjectWithUser
from datetime import date
from typing import Optional, List

class Agreement(BaseModel):
    id: int
    start_date: date
    end_date: date
    current: bool
    status: str  # AgreementStatus
    external_entity: Optional[User] = None  # exEntity/student
    project: Optional[ProjectWithUser] = None  # Opcional

class AgreementCreate(BaseModel):
    start_date: date
    end_date: date
    user_id: Optional[int] = None  # Agregar campo opcional

class AgreementUpdate(BaseModel):
    """Schema para actualización de convenios"""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current: Optional[bool] = None
    status: Optional[str] = None
        
class AgreementApproval(BaseModel):
    """Schema para aprobación de convenios"""
    status: Optional[str] = None
    current: Optional[bool] = None