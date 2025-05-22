from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schema.workplan_schema import WorkPlan, WorkPlanCreate
from services.project_service import ProjectService
from schema.project_schema import Project, ProjectCreate
from db.db import SessionLocal

project_router = APIRouter(prefix="/projects", tags=["projects"])
project_service = ProjectService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@project_router.post("/create", response_model=Project)
def create(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        created_project = project_service.create_project(db, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_project

@project_router.get("/", response_model=list[Project])
def list_projects(db: Session = Depends(get_db)):
    return project_service.list_projects(db)

@project_router.get("/{idUser}", response_model=list[Project])
def list_projects_by_user(idUser: int, db: Session = Depends(get_db)):
    return project_service.list_projects_by_user(idUser, db)

@project_router.post("/assignUserToProject", response_model=dict)
def assign_user_to_project(user_id: int, project_id: int, user_to_assign: int,db: Session = Depends(get_db)):
    try:
        project_service.assign_user_to_project(db, project_id, user_id, user_to_assign)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Usuario asignado con exito"}