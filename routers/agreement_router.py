from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from db.db import SessionLocal
from schemas.agreements_schema import Agreement, AgreementCreate, AgreementUpdate
from schemas.project_schema import ProyectComplete
from services.agreement_service import AgreementService

agreement_router = APIRouter(prefix="/agreements", tags=["agreements"])
agreement_service = AgreementService()

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@agreement_router.post("/", response_model=Agreement, status_code=status.HTTP_201_CREATED)
def create_agreement(agreement: AgreementCreate, db: Session = Depends(get_db)) -> Agreement:
    """Crea un nuevo convenio"""
    try:
        # Validar fechas antes de crear
        if agreement.start_date > agreement.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="La fecha de inicio debe ser anterior a la fecha de fin"
            )
        
        created_agreement = agreement_service.create_agreement(db, agreement)
        return created_agreement
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error interno: {e}")  # Para debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error interno del servidor: {str(e)}"
        )

@agreement_router.get("/", response_model=List[Agreement], 
                     summary="Listar todos los convenios", description="Obtiene una lista de todos los convenios")
def list_all_agreements(db: Session = Depends(get_db)) -> List[Agreement]:
    """Lista todos los convenios"""
    try:
        agreements = agreement_service.list_agreements(db)
        return agreements
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail="Error interno del servidor")


@agreement_router.get("/pending", response_model=List[Agreement], 
                     summary="Listar convenios pendientes", description="Obtiene convenios pendientes de aprobación")
def list_pending_agreements(db: Session = Depends(get_db)) -> List[Agreement]:
    """Lista convenios pendientes de aprobación"""
    try:
        pending_agreements = agreement_service.list_pending_agreements(db)
        return pending_agreements
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail="Error interno del servidor")


@agreement_router.get("/{agreement_id}", response_model=Agreement, 
                     summary="Obtener convenio por ID", description="Obtiene un convenio específico por su ID")
def get_agreement_by_id(agreement_id: int, db: Session = Depends(get_db)) -> Agreement:
    """Obtiene un convenio por ID"""
    try:
        agreement = agreement_service.get_agreement_by_id(db, agreement_id)
        return agreement
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail="Error interno del servidor")

@agreement_router.put("/{agreement_id}", response_model=Agreement, 
                     summary="Actualizar convenio", description="Actualiza un convenio existente")
def update_agreement(agreement_id: int, update_data: AgreementUpdate, 
                    db: Session = Depends(get_db)) -> Agreement:
    """Actualiza un convenio existente"""
    try:
        updated_agreement = agreement_service.update_agreement(db, agreement_id, update_data)
        return updated_agreement
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail="Error interno del servidor")

@agreement_router.delete("/{agreement_id}", response_model=dict, 
                        summary="Eliminar convenio", description="Elimina un convenio del sistema")
def delete_agreement(agreement_id: int, db: Session = Depends(get_db)) -> None:
    """Elimina un convenio"""
    try:
        success = agreement_service.delete_agreement(db, agreement_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail=f"Convenio con ID {agreement_id} no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail="Error interno del servidor")

@agreement_router.patch("/{agreement_id}/approve", response_model=Agreement, 
                       summary="Aprobar convenio", description="Aprueba un convenio pendiente")
def approve_agreement(agreement_id: int, approved_by_id: Optional[int] = Query(None), 
                     db: Session = Depends(get_db)) -> Agreement:
    """Aprueba un convenio"""
    try:
        approved_agreement = agreement_service.approve_agreement(db, agreement_id, approved_by_id)
        return approved_agreement
    except ValueError as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail="Error interno del servidor")

@agreement_router.get("/{agreement_id}", response_model=ProyectComplete, 
                     summary="Obtener proyecto por ID del convenio", description="Obtiene el proyecto completo por el id del convenio")
def get_agreement_by_id(agreement_id: int, db: Session = Depends(get_db)) -> Agreement:
    """Obtiene un convenio por ID"""
    try:
        agreement = agreement_service.get_project_for_agreement(db, agreement_id)
        return agreement
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail="Error interno del servidor")


"""
@agreement_router.patch("/{agreement_id}/reject", response_model=Agreement, 
                       summary="Rechazar convenio", description="Rechaza un convenio pendiente")
def reject_agreement(agreement_id: int, rejection_reason: Optional[str] = Query(None), 
                    db: Session = Depends(get_db)) -> Agreement:
    #Rechaza un convenio
    try:
        rejected_agreement = agreement_service.reject_agreement(db, agreement_id, rejection_reason)
        return rejected_agreement
    except ValueError as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail="Error interno del servidor")
"""

@agreement_router.patch("/{agreement_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT,
                       summary="Desactivar convenio", description="Desactiva un convenio activo")
def deactivate_agreement(agreement_id: int, db: Session = Depends(get_db)) -> None:
    """Desactiva un convenio"""
    try:
        success = agreement_service.deactivate_agreement(db, agreement_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail=f"Convenio con ID {agreement_id} no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail="Error interno del servidor")

@agreement_router.patch("/{agreement_id}/assign-representative/{user_id}", response_model=Agreement,
                       summary="Asignar representante externo", 
                       description="Asigna un representante de entidad externa al convenio")
def assign_external_representative(agreement_id: int, user_id: int, 
                                 db: Session = Depends(get_db)) -> Agreement:
    """Asigna un representante externo al convenio"""
    try:
        updated_agreement = agreement_service.assign_external_representative(db, agreement_id, user_id)
        return updated_agreement
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                          detail="Error interno del servidor")