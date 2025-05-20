from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.db import BaseDBModel  

class ProjectModel(BaseDBModel):
    __tablename__ = "proyectos_pps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    workplan = relationship(
        "WorkPlan",
        back_populates="project",
        uselist=False
    )