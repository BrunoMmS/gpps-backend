from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.proyectPPS_service import proyectoPPS_service
from schema.proyectPPS_schema import proyect_PPS
from db.db import SessionLocal

proyecto_router = APIRouter(prefix="/proyects", tags=["proyects"])
proyecto_service = proyectoPPS_service()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@proyecto_router.post("/register",response_model=proyect_PPS)
def register(proyecto: proyect_PPS, db: Session = Depends(get_db)):
    try:
        created_proyect = proyecto_service.registrar_usuario(db, proyecto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_proyect

#de momento, hice las clases DAO, pero lo q me falta es implementar los metodos para:
# calcularPorcentajeTotal,calcularPorcentajeHecho,calcularPorcentajeNoHecho
# meter la logica para poder devolver todo en los service, solo hice para proyectPPS
