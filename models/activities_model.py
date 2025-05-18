from sqlalchemy import Column, Integer, String, ForeignKey
from db.db import BaseDBModel 
from sqlalchemy.orm import relationship

class Activities(BaseDBModel):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    duration = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    workplan_id = Column(Integer, ForeignKey("workplan.id"))
    workplan = relationship("WorkPlan", back_populates="activities")

    
