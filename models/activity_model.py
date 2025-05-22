from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.db import BaseDBModel 

class ActivityModel(BaseDBModel):
    __tablename__ = "Activity"

    id = Column(Integer, primary_key=True, index=True)
    duration = Column(Integer, index=True)
    name = Column(String, nullable=False)
    done = Column(Boolean, nullable=False)
    workplan_id = Column(Integer, ForeignKey("Plan_de_Trabajo.id"))

    workplan = relationship(
        "WorkPlan",
        back_populates="activities",
        foreign_keys=[workplan_id] 
    )

    tasks = relationship(
        "TaskModel",
        back_populates="activity",
        cascade="all, delete-orphan"
    )