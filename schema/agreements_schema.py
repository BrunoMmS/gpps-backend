# modelo de Convenios

from datetime import date
from pydantic import BaseModel


class Agreements(BaseModel):
    id: int
    starDate: date
    endDate: date
    current: bool #true --> convenio vigente

    