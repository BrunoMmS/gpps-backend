from datetime import date
from enum import Enum
from typing import Optional
from entities.user_entity import UserEntity

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
                 user_id: Optional[int] = None):  # Agregar user_id
        self._id = id
        self._start_date = start_date
        self._end_date = end_date
        self._current = self._calculate_current_status()
        self._status: AgreementStatus = status or AgreementStatus.PENDING
        self._external_entity = external_entity
        self._user_id = user_id  # Agregar este campo
        self._validate_dates()
    
    def get_user_id(self) -> Optional[int]:
        """Obtiene el ID del usuario asociado"""
        if self._external_entity:
            return self._external_entity.get_id()
        return self._user_id
        
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
    
    def is_current(self) -> bool:
        """Verifica si el convenio está vigente"""
        return self._current
    
    def get_status(self) -> AgreementStatus:
        """Obtiene el estado del convenio"""
        return self._status
    
    def get_external_entity(self) -> Optional[UserEntity]:
        """Obtiene la entidad externa asociada"""
        return self._external_entity
    
    def get_user_id(self) -> Optional[int]:
        """Obtiene el ID del usuario asociado a la entidad externa"""
        return self._external_entity.get_id() if self._external_entity else None
    
    # Métodos de negocio
    def update_dates(self, start_date: date, end_date: date) -> None:
        """Actualiza las fechas del convenio"""
        if start_date > end_date:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
        
        if end_date < date.today():
            raise ValueError("La fecha de fin no puede ser anterior a hoy")
        
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
        
        if rejected_by.get_role() != "admin":
            raise ValueError("Solo administradores UNRN pueden rechazar convenios")
        
        self._status = AgreementStatus.REJECTED
        
    def assign_external_entity(self, external_entity: UserEntity) -> None:
        """Asigna representante de entidad externa al convenio"""
        if external_entity.get_role() != "exEntity":
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
    
    def _validate_dates(self) -> None:
        #Valida fechas
        if self._start_date > self._end_date:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
    
        # Permitir fechas pasadas para convenios históricos
        # if self._end_date < date.today():
        #     raise ValueError("La fecha de fin no puede ser anterior a hoy")
        
    def _can_be_approved(self) -> bool:
        """Verifica si el convenio puede ser aprobado"""
        return self._status == AgreementStatus.PENDING
        
    def _can_be_rejected(self) -> bool:
        """Verifica si el convenio puede ser rechazado"""
        return self._status == AgreementStatus.PENDING
    
    def _is_active(self) -> bool:
        """Verifica si el convenio está activo"""
        return self._status == AgreementStatus.APPROVED and self.is_current()
