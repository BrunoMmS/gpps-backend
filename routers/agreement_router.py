from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas.agreements_schema import AgreementCreate, AgreementUpdate, AgreementResponse, AgreementWithUser
from schemas.project_schema import ProyectComplete
from services.agreement_service import AgreementService
from db.db import SessionLocal

agreement_router = APIRouter(prefix="/agreements", tags=["agreements"])
agreement_service = AgreementService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@agreement_router.post("/", response_model=AgreementResponse)
def create_agreement(agreement: AgreementCreate, creator_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.create_agreement(db, agreement, creator_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@agreement_router.get("/", response_model=List[AgreementResponse])
def list_all_agreements(requester_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.list_agreements(db, requester_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@agreement_router.get("/pending", response_model=List[AgreementResponse])
def list_pending_agreements(requester_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.list_pending_agreements(db, requester_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@agreement_router.get("/created-by/{user_id}", response_model=List[AgreementResponse])
def list_agreements_created_by(user_id: int, requester_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return agreement_service.list_agreements_by_creator(db, user_id, requester_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@agreement_router.get("/{agreement_id}", response_model=AgreementResponse)
def get_agreement_by_id(agreement_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.get_agreement_by_id(db, agreement_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@agreement_router.put("/{agreement_id}", response_model=AgreementResponse)
def update_agreement(agreement_id: int, update_data: AgreementUpdate, updater_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.update_agreement(db, agreement_id, update_data, updater_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@agreement_router.delete("/{agreement_id}")
def delete_agreement(agreement_id: int, deleter_id: int, db: Session = Depends(get_db)):
    try:
        agreement_service.delete_agreement(db, agreement_id, deleter_id)
        return {"detail": "Convenio eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@agreement_router.patch("/{agreement_id}/approve", response_model=AgreementResponse)
def approve_agreement(agreement_id: int, approved_by_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.approve_agreement(db, agreement_id, approved_by_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@agreement_router.patch("/{agreement_id}/reject", response_model=AgreementResponse)
def reject_agreement(agreement_id: int, rejected_by_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.reject_agreement(db, agreement_id, rejected_by_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@agreement_router.patch("/{agreement_id}/assign-user", response_model=AgreementResponse)
def assign_user_to_agreement(agreement_id: int, user_id: int, assigner_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.assign_user_to_agreement(db, agreement_id, user_id, assigner_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@agreement_router.get("/with-project/{agreement_id}", response_model=ProyectComplete)
def list_agreement_with_project(agreement_id: int, requester_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.list_agreement_with_project(db, agreement_id, requester_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@agreement_router.get("/current", response_model=List[AgreementResponse])
def get_current_agreements(requester_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.get_current_agreements(db, requester_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@agreement_router.get("/expired", response_model=List[AgreementResponse])
def get_expired_agreements(requester_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.get_expired_agreements(db, requester_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@agreement_router.patch("/{agreement_id}/assign-project", response_model=AgreementResponse)
def assign_project_to_agreement(agreement_id: int, project_id: int, assigner_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.assign_project_to_agreement(db, agreement_id, project_id, assigner_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@agreement_router.get("/with-user/{user_id}", response_model=list[AgreementWithUser])
def get_agreement_with_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return agreement_service.get_all_agreements_with_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")