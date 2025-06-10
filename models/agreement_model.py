from datetime import date
from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from db.db import BaseDBModel

class AgreementModel(BaseDBModel):
    __tablename__ = "convenios"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    user_id = Column(Integer, ForeignKey("Usuarios.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("proyectos_pps.id"))

    user = relationship("UserModel", back_populates="agreements")
    project = relationship("ProjectModel", back_populates="agreements")
    
    #esto me parece que no es necesario, ya que el proyecto es una relación uno a uno lo conservo para el futuro
    #project_id = Column(Integer, ForeignKey("proyectos.id"), nullable=True)
    #def __repr__(self):
    #    return f"<AgreementModel(id={self.id}, status={self.status}, current={self.current})>"