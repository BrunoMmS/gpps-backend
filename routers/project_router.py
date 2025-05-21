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

@project_router.post("/register", response_model=Project)
def register(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        created_project = project_service.register_user(db, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_project

@project_router.post("/create", response_model=Project)
def create(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        created_project = project_service.create_project(db, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_project

@project_router.post("/create_workplan", response_model=WorkPlan)
def add_workplan(workplan: WorkPlanCreate,db: Session = Depends(get_db)):
    try:
        workplan = project_service.add_workplan(db, workplan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return workplan
#de momento, hice las clases DAO, pero lo q me falta es implementar los metodos para:
# calcularPorcentajeTotal,calcularPorcentajeHecho,calcularPorcentajeNoHecho
# meter la logica para poder devolver todo en los service, solo hice para proyectPPS

@project_router.get("/assignUserToProject/{project_id}/{user_id}/{user_to_assign}", response_model=dict)
def assign_user_to_project(user_id: int, project_id: int, user_to_assign: int,db: Session = Depends(get_db)):
    try:
        project_service.assign_user_to_project(db, project_id, user_id, user_to_assign)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Usuario asignado con exito"}