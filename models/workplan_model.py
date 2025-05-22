from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.db import BaseDBModel 

class WorkPlan(BaseDBModel):
    __tablename__ = "Plan_de_Trabajo"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("proyectos_pps.id"), nullable=False)
    description = Column(String, nullable=False)
    project = relationship(
        "ProjectModel",
        back_populates="workplan"
    )
    
    activities = relationship(
        "ActivityModel",
        back_populates="workplan",
        cascade="all, delete-orphan"
    )