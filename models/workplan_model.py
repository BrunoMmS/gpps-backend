from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from db.db import BaseDBModel 

class WorkPlan(BaseDBModel):
    __tablename__ = "Plan_de_Trabajo"

    id = Column(Integer, primary_key=True, index=True)

    project = relationship("ProjectModel", back_populates="workplan", uselist=False)

    activities = relationship("ActivitieModel", back_populates="workplan")