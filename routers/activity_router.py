from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.db import SessionLocal
from schemas.activity_schema import ActivitieCreate, Activitie
from schemas.task_schema import TaskCreate
from services.activity_service import ActivityService

activity_router = APIRouter(prefix="/activity", tags=["activity"])
activity_service = ActivityService()

def get_db():
    db = SessionLocal()
    try:
        yield db    
    finally:
        db.close()


@activity_router.post("/create")
def create_activity(
    workplan_id: int,
    activity_data: ActivitieCreate,
    db: Session = Depends(get_db)
):
    try:
        created_activity = activity_service.create_activity(db, workplan_id, activity_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_activity


@activity_router.post("/{activity_id}/task/create")
def create_task_for_activity(
    activity_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    try:
        created_task = activity_service.append_task(db, activity_id, task_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return created_task


@activity_router.get("/workplan/{workplan_id}", response_model=list[Activitie])
def get_activities_by_workplan(
    workplan_id: int,
    db: Session = Depends(get_db)
):
    return activity_service.get_activities_by_workplan(db, workplan_id)