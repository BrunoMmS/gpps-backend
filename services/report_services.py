from pytest import Session
from entities.report_entity import ReportEntity
from services.project_service import ProjectService
from services.workplan_service import WorkPlanService


class ReportService:
    def __init__(self, workplan_service: WorkPlanService, project_service: ProjectService):
        self.workplan_service = workplan_service
        self.project_service = project_service

    def generate_project_report(self, db: Session, proyect_id: int) -> str:
        proyect_model = self.project_service.project_dao.get_proyect_complete(db, proyect_id)
        if not proyect_model:
            raise ValueError("Proyecto no encontrado")

        project_entity = self.project_service.proyect_to_entity(proyect_model)
        workplan_entity = self.workplan_service.workplan_to_entity(proyect_model.workplan, project_entity)

        report = ReportEntity(project_entity, workplan_entity)
        return "\n".join(report.generate_lines())
