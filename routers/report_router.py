
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from db.db import SessionLocal
from services.report_services import ReportService
from services.project_service import ProjectService
from services.workplan_service import WorkPlanService

report_router = APIRouter(prefix="/report", tags=["report"])

project_service = ProjectService()
workplan_service = WorkPlanService()
report_service = ReportService(workplan_service, project_service)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@report_router.get("/project/{idProject}", response_class=PlainTextResponse)
def get_report_with_id(idProject: int, db: Session = Depends(get_db)):
    try:
        report = report_service.generate_project_report(db, idProject)
        return report
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
