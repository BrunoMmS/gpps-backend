# modelo de Convenios
from datetime import date

from pydantic import BaseModel

class Agreement(BaseModel):
    id: int
    starDate: date
    endDate: date
    current: bool #true --> convenio vigente
    projects: list[Project]
    #firm1: exEntity/student

class AgreementCreate(Agreement):
    pass

class AgreementUpdate(Agreement):
    current: bool | None = None
    reasonRejection: str | None = None

class Agreement(Agreement):
    id: int
    current: bool | None = None
    reasonRejection: str | None = None

    class Config:
        orm_mode = True