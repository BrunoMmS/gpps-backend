from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.project_service import ProjectService
from schema.project_schema import Project
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
def register(project: Project, db: Session = Depends(get_db)):
    try:
        created_project = project_service.register_user(db, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_project

#de momento, hice las clases DAO, pero lo q me falta es implementar los metodos para:
# calcularPorcentajeTotal,calcularPorcentajeHecho,calcularPorcentajeNoHecho
# meter la logica para poder devolver todo en los service, solo hice para proyectPPS