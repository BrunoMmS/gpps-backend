from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.db import BaseDBModel
from entities.agreement_entity import AgreementEntity, AgreementStatus

class AgreementModel(BaseDBModel):
    __tablename__ = "convenios"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(20), default=AgreementStatus.PENDING.value, nullable=False)

    created_by = Column(Integer, ForeignKey("Usuarios.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("Usuarios.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("proyectos_pps.id"), nullable=True)

    user = relationship("UserModel", foreign_keys=[user_id], back_populates="assigned_agreements")
    created_by_user = relationship("UserModel", foreign_keys=[created_by], back_populates="created_agreements")

    project = relationship("ProjectModel", back_populates="agreements")

    def is_current(self) -> bool:
        """Indica si el convenio está vigente hoy."""
        today = date.today()
        return self.start_date <= today <= self.end_date

    def is_expired(self) -> bool:
        """Indica si el convenio está vencido."""
        return date.today() > self.end_date

    def to_entity(self) -> AgreementEntity:
        """Convierte el modelo en una entidad de dominio."""
        return AgreementEntity(
            id=self.id,
            start_date=self.start_date,
            end_date=self.end_date,
            created_by=self.created_by,
            user_id=self.user_id,
            project_id=self.project_id,
            status=AgreementStatus(self.status)
        )

    def update_from_entity(self, entity: AgreementEntity) -> None:
        """Actualiza el modelo a partir de una entidad de dominio."""
        self.start_date = entity.get_start_date()
        self.end_date = entity.get_end_date()
        self.created_by = entity.get_created_by()
        self.user_id = entity.get_user_id()
        self.project_id = entity.get_project_id()
        self.status = entity.get_status().value

    @staticmethod
    def from_entity(entity: AgreementEntity) -> 'AgreementModel':
        """Crea un modelo a partir de una entidad de dominio."""
        return AgreementModel(
            start_date=entity.get_start_date(),
            end_date=entity.get_end_date(),
            created_by=entity.get_created_by(),
            user_id=entity.get_user_id(),
            project_id=entity.get_project_id(),
            status=entity.get_status().value
        )

    
    #esto me parece que no es necesario, ya que el proyecto es una relación uno a uno lo conservo para el futuro
    #project_id = Column(Integer, ForeignKey("proyectos.id"), nullable=True)
    #def __repr__(self):
    #    return f"<AgreementModel(id={self.id}, status={self.status}, current={self.current})>"