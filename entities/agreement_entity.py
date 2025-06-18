from datetime import date
from enum import Enum
from typing import Optional
from entities.user_entity import UserEntity
from roles.rol import Rol

class AgreementStatus(str, Enum):
    """Estados posibles de un convenio"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    # ACTIVE = "active"
    # INACTIVE = "inactive"  # Descomentar si se desea usar


class AgreementEntity:
    def __init__(
        self,
        start_date: date,
        end_date: date,
        id: Optional[int] = None,
        created_by: Optional[int] = None,
        user_id: Optional[int] = None,
        project_id: Optional[int] = None,
        status: AgreementStatus = AgreementStatus.PENDING,
    ):
        self._validate_dates(start_date, end_date)
        self._id = id
        self._start_date = start_date
        self._end_date = end_date
        self._created_by = created_by
        self.user_id = user_id    
        self._project_id = project_id
        self._status = status

    # ---------------------------
    # Propiedades públicas (Getters)
    # ---------------------------
    @property
    def get_id(self) -> Optional[int]:
        return self._id

    @property
    def get_start_date(self) -> date:
        return self._start_date

    @property
    def get_end_date(self) -> date:
        return self._end_date

    @property
    def get_created_by(self) -> Optional[int]:
        return self._created_by

    @property
    def get_user_id(self) -> Optional[int]:
        return self.user_id

    @property
    def get_project_id(self) -> Optional[int]:
        return self._project_id

    @property
    def get_status(self) -> AgreementStatus:
        return self._status

    @property
    def is_current(self) -> bool:
        today = date.today()
        return self.get_start_date <= today <= self.get_end_date

    @property
    def is_expired(self) -> bool:
        return date.today() > self.get_end_date

    # ---------------------------
    # Métodos de negocio
    # ---------------------------
    def approve(self, approved_by: UserEntity) -> None:
        self._validate_can_be_approved(approved_by)
        self._status = AgreementStatus.APPROVED

    def reject(self, rejected_by: UserEntity) -> None:
        self._validate_can_be_rejected(rejected_by)
        self._status = AgreementStatus.REJECTED

    def update_dates(self, new_start: date, new_end: date) -> None:
        self._validate_dates(new_start, new_end)
        self._start_date = new_start
        self._end_date = new_end

    def to_expire(self) -> None:
        if self.is_expired and self._status not in [AgreementStatus.EXPIRED]:
            self._status = AgreementStatus.EXPIRED

    def assign_user_id(self, user: UserEntity) -> None:
        self._validate_user(user)
        self.user_id = user.getId()

    # ---------------------------
    # Métodos privados
    # ---------------------------
    def _validate_dates(self, start: date, end: date) -> None:
        if start > end:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin.")
        if end < date.today():
            raise ValueError("La fecha de fin no puede ser anterior a hoy.")

    def _validate_can_be_approved(self, user: UserEntity) -> None:
        if self._status not in [AgreementStatus.PENDING, AgreementStatus.REJECTED]:
            raise ValueError("Solo convenios pendientes o rechazados pueden ser aprobados.")
        self._validate_user(user)

    def _validate_user(self, user: UserEntity) -> None:
        # valida que el usuario tenga rol correcto
        if user.getRole() not in [Rol.admin, Rol.exEntity]:
            raise ValueError("No tienes el permiso para realizar esta accion en convenios.")

    def _validate_can_be_rejected(self, user: UserEntity) -> None:
        if self._status != AgreementStatus.PENDING:
            raise ValueError("Solo convenios pendientes pueden ser rechazados.")
        self._validate_user(user)