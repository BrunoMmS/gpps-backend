from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.db import BaseDBModel
#from entities.agreement_entity import AgreementEntity  #<-- Descomentar si se usan metodos al final

class AgreementModel(BaseDBModel):
    __tablename__ = "convenios"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(20), default="pending", nullable=False)

    # Relacion 1-1
    user_id = Column(Integer, ForeignKey("Usuarios.id"), nullable=True)

    # Relacion 1-1
    project_id = Column(Integer, ForeignKey("proyectos_pps.id"), nullable=True)

    user = relationship("UserModel", back_populates="agreements")
    project = relationship("ProjectModel", back_populates="agreements")

    def is_current(self) -> bool:
        """Convenio vigente en la fecha actual"""
        today = date.today()
        return self.start_date <= today <= self.end_date

    def is_expired(self) -> bool:
        """Convenio expirado (fecha fin pasada)"""
        return date.today() > self.end_date
    
    #esto me parece que no es necesario, ya que el proyecto es una relación uno a uno lo conservo para el futuro
    #project_id = Column(Integer, ForeignKey("proyectos.id"), nullable=True)
    #def __repr__(self):
    #    return f"<AgreementModel(id={self.id}, status={self.status}, current={self.current})>"
    
    '''

    def to_entity(self) -> AgreementEntity:
        return AgreementEntity(
            id=self.id,
            start_date=self.start_date,
            end_date=self.end_date,
            external_entity_id=self.user_id,
            project_id=self.project_id,
            status=self.status
        )

    def update_from_entity(self, entity: AgreementEntity) -> None:
        self.start_date = entity.get_start_date
        self.end_date = entity.get_end_date
        self.status = entity.get_status
        self.user_id = entity.get_external_entity_id
        self.project_id = entity.get_project_id

    @staticmethod
    def from_entity(entity: AgreementEntity) -> 'AgreementModel':
        return AgreementModel(
            id=entity.get_id,
            start_date=entity.get_start_date,
            end_date=entity.get_end_date,
            status=entity.get_status,
            user_id=entity.get_external_entity_id,
            project_id=entity.get_project_id
        )
    
    '''