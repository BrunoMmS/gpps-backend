from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from db.db import BaseDBModel 

class WorkPlan(BaseDBModel):
    __tablename__ = "workplan"

    id = Column(Integer, primary_key=True, index=True)

    project = relationship("ProyectPPS", back_populates="workplan", uselist=False)

    activities = relationship("Activities", back_populates="workplan")
