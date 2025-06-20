from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.workplan_schema import WorkPlan, WorkPlanCreate
from services.project_service import ProjectService
from schemas.project_schema import Project, ProjectCreate, ProyectComplete, ProjectWithUser
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

@project_router.put("/approve/{project_id}", response_model=Project)
def approve(project_id: int, db: Session = Depends(get_db)):
    try:
        project = project_service.approve_project(db, project_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return project

@project_router.get("/", response_model=list[Project])
def list_projects(db: Session = Depends(get_db)):
    return project_service.list_projects(db)

@project_router.get("/{idUser}", response_model=list[Project])
def list_projects_by_user(idUser: int, db: Session = Depends(get_db)):
    try:
        return project_service.list_projects_by_user(idUser, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@project_router.post("/assignUserToProject", response_model=dict)
def assign_user_to_project(user_id: int, project_id: int, user_to_assign: int,db: Session = Depends(get_db)):
    try:
        project_service.assign_user_to_project(db, project_id, user_id, user_to_assign)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Usuario asignado con exito"}
@project_router.get("/projects/{project_id}/complete", response_model=ProyectComplete)
def get_project_complete(project_id: int, db: Session = Depends(get_db)):
    try:
        return project_service.get_complete_project(db, project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@project_router.get("/{user_id}/complete", response_model=list[ProyectComplete])
def get_project_complete_by_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return project_service.get_complete_project_by_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))    

@project_router.get("/project/getProjectWithUser/{idProject}", response_model = ProjectWithUser)
def get_project_with_user(idProject: int, db: Session = Depends(get_db)):
    try:
        project = project_service.get_project_with_user(db, idProject)
        if not project:
            raise HTTPException(status_code=404, detail="Projecto no encontrado")
        return project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@project_router.get("/getProjectsWithUser/{idUser}", response_model = list[ProjectWithUser])
def get_projects_with_user(idUser: int, db: Session = Depends(get_db)):
    try:
        return project_service.get_projects_with_user(db, idUser)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@project_router.get("/all/WithUser", response_model=list[ProjectWithUser])
def get_all_projects_with_user(db: Session = Depends(get_db)):
    try:
     return project_service.get_all_projects_with_user(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@project_router.post("/workplan/assign", response_model=WorkPlan)
def assign_workplan_to_project(user_id: int, workplan: WorkPlanCreate, db: Session = Depends(get_db)):
    try:
        return project_service.add_workplan(db, user_id,workplan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@project_router.get("/getProjectsToAssign/", response_model = list[ProjectWithUser])
def get_projects_with_user(db: Session = Depends(get_db)):
    try:
        return project_service.get_all_projects_to_assign_with_user(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))