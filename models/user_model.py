# models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.db import BaseDBModel

class UserModel(BaseDBModel):
    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_projects = relationship("ProjectModel", back_populates="creator")

    projects = relationship(
        "UserInProjectModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    agreements = relationship("AgreementModel", back_populates="user")