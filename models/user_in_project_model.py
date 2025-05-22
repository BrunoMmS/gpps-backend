# models/user_in_project.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.db import BaseDBModel

class UserInProjectModel(BaseDBModel):
    __tablename__ = "user_in_project"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Usuarios.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("proyectos_pps.id"), nullable=False)

    user = relationship(
        "UserModel",
        back_populates="projects"
    )
    project = relationship(
        "ProjectModel",
        back_populates="users"
    )
