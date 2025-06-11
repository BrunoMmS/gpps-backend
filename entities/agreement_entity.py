from datetime import date
from enum import Enum
from typing import Optional
from entities.user_entity import UserEntity

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
        external_entity_id: Optional[int] = None,
        project_id: Optional[int] = None,
        status: AgreementStatus = AgreementStatus.PENDING,
    ):
        self._validate_dates(start_date, end_date)
        self._id = id
        self._start_date = start_date
        self._end_date = end_date
        self._external_entity_id = external_entity_id
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
    def get_external_entity_id(self) -> Optional[int]:
        return self._external_entity_id

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

    def assign_external_entity(self, user: UserEntity) -> None:
        if user.getRole() != "ExternalEntity":
            raise ValueError("El usuario debe tener rol de entidad externa.")
        self._external_entity_id = user.getId()

    def update_dates(self, new_start: date, new_end: date) -> None:
        self._validate_dates(new_start, new_end)
        self._start_date = new_start
        self._end_date = new_end

    def update_status(self, new_status: AgreementStatus) -> None:
        self._status = new_status

    # ---------------------------
    # Métodos privados
    # ---------------------------
    def _validate_dates(self, start: date, end: date) -> None:
        if start > end:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin.")
        if end < date.today():
            raise ValueError("La fecha de fin no puede ser anterior a hoy.")

    def _validate_can_be_approved(self, user: UserEntity) -> None:
        if self._status != AgreementStatus.PENDING:
            raise ValueError("Solo convenios pendientes pueden ser aprobados.")
        if user.getRole() != "Administrator":
            raise ValueError("Solo administradores pueden aprobar convenios.")

    def _validate_can_be_rejected(self, user: UserEntity) -> None:
        if self._status != AgreementStatus.PENDING:
            raise ValueError("Solo convenios pendientes pueden ser rechazados.")
        if user.get_role() != "Administrator":
            raise ValueError("Solo administradores pueden rechazar convenios.")
