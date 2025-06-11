from pydantic import BaseModel, model_validator
from datetime import date
from typing import Optional
from entities.agreement_entity import AgreementStatus  # Enum definido

class Agreement(BaseModel):
    id: int
    start_date: date
    end_date: date
    current: Optional[bool] = None
    status: AgreementStatus
    user_id: Optional[int]
    project_id: Optional[int]
    
class AgreementResponse(Agreement):
    pass

class AgreementCreate(BaseModel):
    start_date: date
    end_date: date
    user_id: Optional[int] = None

class AgreementUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[AgreementStatus] = None
    user_id: Optional[int] = None
    project_id: Optional[int] = None

class AgreementApproval(BaseModel):
    status: AgreementStatus