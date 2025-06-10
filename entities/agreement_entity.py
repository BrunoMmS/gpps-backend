from datetime import date
from enum import Enum
from typing import Optional
from entities.user_entity import UserEntity
from entities.project_entity import ProjectEntity

class AgreementStatus(str, Enum):
    """Estados del convenio"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    
class AgreementEntity:
    def __init__(self, id: Optional[int], start_date: date, end_date: date, 
                 external_entity: Optional[UserEntity] = None, 
                 status: Optional[AgreementStatus] = None,
                 a_project: Optional[ProjectEntity] = None):  # Agregar user_id
        self._id = id
        self._start_date = start_date
        self._end_date = end_date
        self._current = self._calculate_current_status()
        self._status: AgreementStatus = status or AgreementStatus.PENDING
        self._external_entity = external_entity
        self._project = a_project  # Agregar este campo
        
    # Getters públicos
    def get_id(self) -> Optional[int]:
        """Obtiene el ID del convenio"""
        return self._id
    
    def get_start_date(self) -> date:
        """Obtiene la fecha de inicio"""
        return self._start_date
    
    def get_end_date(self) -> date:
        """Obtiene la fecha de fin"""
        return self._end_date
    
    def get_status(self) -> AgreementStatus:
        """Obtiene el estado del convenio"""
        return self._status
    
    def get_idProject(self) -> Optional[int]:
        """Obtiene el ID del proyecto asociado al convenio"""
        return self._project.get_id() if self._project else None
    
    def get_idExternalUser(self) -> Optional[int]:
        """Obtiene el ID del usuario asociado"""
        if self._external_entity:
            return self._external_entity.getId() if self._external_entity else None
    
    # Métodos de negocio
    def update_dates(self, start_date: date, end_date: date) -> None:
        self.validate_date(start_date, end_date)
        
        self._start_date = start_date
        self._end_date = end_date
        self._current = self._calculate_current_status()
    
    def approve(self, approved_by: UserEntity) -> None:
        """Aprueba el convenio"""
        if not self._can_be_approved():
            raise ValueError("Solo se pueden aprobar convenios pendientes")
        
        if approved_by.get_role() != "admin":
            raise ValueError("Solo administradores UNRN pueden aprobar convenios")
        
        self._status = AgreementStatus.APPROVED
        
    def reject(self, rejected_by: UserEntity, reason: Optional[str] = None) -> None:
        """Rechaza el convenio"""
        if not self._can_be_rejected():
            raise ValueError("Solo se pueden rechazar convenios pendientes")
        
        if rejected_by.getRole() != "Administrator":
            raise ValueError("Solo administradores UNRN pueden rechazar convenios")
        
        self._status = AgreementStatus.REJECTED
        
    def assign_external_entity(self, external_entity: UserEntity) -> None:
        """Asigna representante de entidad externa al convenio"""
        if external_entity.getRole() != "ExternalEntity":
            raise ValueError("El usuario debe tener rol de entidad externa")
        
        self._external_entity = external_entity
    
    def update_status(self, status: AgreementStatus) -> None:
        """Actualiza el estado del convenio"""
        self._status = status
        
    def activate(self) -> None:
        """Activa el convenio"""
        if self._status != AgreementStatus.APPROVED:
            raise ValueError("Solo se pueden activar convenios aprobados")
        self._status = AgreementStatus.ACTIVE
        
    def deactivate(self) -> None:
        """Desactiva el convenio"""
        if self._status not in [AgreementStatus.ACTIVE, AgreementStatus.APPROVED]:
            raise ValueError("Solo se pueden desactivar convenios activos o aprobados")
        self._status = AgreementStatus.INACTIVE
        self._current = False
    
    # Métodos privados
    def _calculate_current_status(self) -> bool:
        """Calcula si el convenio está vigente según las fechas"""
        today = date.today()
        return self._start_date <= today <= self._end_date
    
    def _check_expiration(self) -> None:
        """Verifica y actualiza el estado si el convenio expiró"""
        if (self._status == AgreementStatus.APPROVED and 
            date.today() > self._end_date):
            self._status = AgreementStatus.EXPIRED
        
    def _can_be_approved(self) -> bool:
        """Verifica si el convenio puede ser aprobado"""
        return self._status == AgreementStatus.PENDING
        
    def _can_be_rejected(self) -> bool:
        """Verifica si el convenio puede ser rechazado"""
        return self._status == AgreementStatus.PENDING
    
    def _is_active(self) -> bool:
        """Verifica si el convenio está activo"""
        return self._status == AgreementStatus.APPROVED and self.is_current()
    
    def _validate_date(self, start_date, end_date):
        """Actualiza las fechas del convenio"""
        if start_date > end_date:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
        
        if end_date < date.today():
            raise ValueError("La fecha de fin no puede ser anterior a hoy")
