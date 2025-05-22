# models/project.py (o donde lo tengas)
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.db import BaseDBModel

class ProjectModel(BaseDBModel):
    __tablename__ = "proyectos_pps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    active = Column(Boolean, default=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    users = relationship(
        "UserInProjectModel",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    workplan = relationship(
        "WorkPlan",
        back_populates="project",
        uselist=False
    )
