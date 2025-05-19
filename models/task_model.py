from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from db.db import BaseDBModel 
from sqlalchemy.orm import relationship

class TaskModel(BaseDBModel):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    done = Column(Boolean, nullable=False, default=False)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    activity = relationship("Activities", back_populates="tasks")
    