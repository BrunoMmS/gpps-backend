# modelo de Convenios

class Agreements(BaseModel):
    id: int
    starDate: date
    endDate: date
    current: bool #true --> convenio vigente

    