from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from db.db import SessionLocal
from schema.workplan_schema import WorkPlan, WorkPlanCreate
from services.workplan_service import WorkPlanService



workplan_router = APIRouter(prefix="/workplan", tags=["workplan"])
workplan_service = WorkPlanService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@workplan_router.post("/create", response_model=WorkPlan)
def create_workplan(user_id: int, workplan_data: WorkPlanCreate, db: Session = Depends(get_db)):
    try:
        created_workplan = workplan_service.create_workplan(db, user_id, workplan_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_workplan