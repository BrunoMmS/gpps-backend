from pydantic import BaseModel
from schemas.user_schema import User 
from schemas.project_schema import ProjectWithUser
from datetime import date
from typing import Optional, List

class Agreement(BaseModel):
    id: int
    start_date: date
    end_date: date
    current: Optional[bool] = None
    status: str  # AgreementStatus
    user_id: Optional[User] = None  # exEntity opcional
    project: Optional[ProjectWithUser] = None  # Opcional puede o no tener un proyecto asignado

class AgreementCreate(BaseModel):
    start_date: date
    end_date: date
    user_id: Optional[int]  # Agregar entidad externa

class AgreementUpdate(BaseModel):
    """Schema para actualización de convenios"""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    user_id: Optional[int] = None
    project: Optional[ProjectWithUser] = None
        
class AgreementApproval(BaseModel):
    """Schema para aprobación de convenios"""
    status: Optional[str] = None
    current: Optional[bool] = None