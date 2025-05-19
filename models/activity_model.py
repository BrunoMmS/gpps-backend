from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from db.db import BaseDBModel 
from sqlalchemy.orm import relationship
#from schema.activity_schema import ActivityCreate

class ActivityModel(BaseDBModel):
    __tablename__ = "Activity"

    id = Column(Integer, primary_key=True, index=True)
    duration = Column(Integer,  index=True)
    name = Column(String, nullable=False)
    done = Column(Boolean, nullable=False)
    workplan_id = Column(Integer, ForeignKey("Plan_de_Trabajo.id"))
    workplan = relationship("WorkPlan", back_populates="activity")
    tasks = relationship("Task", back_populates="activity")