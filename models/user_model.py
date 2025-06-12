# models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from db.db import BaseDBModel
from roles.rol import Rol

class UserModel(BaseDBModel):
    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLEnum(Rol, values_callable=lambda x: [e.value for e in x]), default=Rol.student.value, nullable=False)
    created_projects = relationship("ProjectModel", back_populates="creator")

    projects = relationship(
        "UserInProjectModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    agreements = relationship("AgreementModel", back_populates="user")