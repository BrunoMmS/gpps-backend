from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.db import BaseDBModel 

class TaskModel(BaseDBModel):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    done = Column(Boolean, nullable=False, default=False)
    activity_id = Column(Integer, ForeignKey("Activity.id"))

    activity = relationship(
        "ActivityModel",
        back_populates="tasks"
    )
