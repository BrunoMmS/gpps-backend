from sqlalchemy.orm import Session
from cruds.workplanDAO import WorkPlanDAO
from schemas.workplan_schema import WorkPlanCreate
from services.activity_service import ActivityService
from services.rol import Rol
from services.user_service import UserService
from entities.workplan_entity import WorkplanEntity
from models.workplan_model import WorkPlan
from entities.project_entity import ProjectEntity

class WorkPlanService:
    def __init__(self):
        self.workplan_dao = WorkPlanDAO()
        self.user_service = UserService()
        self.activity_service = ActivityService()

    def create_workplan(self, db: Session, user_id: int, workplan_data: WorkPlanCreate) -> WorkPlanCreate:
        user = self.user_service.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        userEntity = self.user_service.to_entity(user)
        if userEntity.getRole() not in [Rol.student, Rol.teacher2]:
            raise ValueError("El usuario no tiene permisos para crear un plan de trabajo")
        
        return self.workplan_dao.create(db, workplan_data)
    
    def workplan_to_entity(self, workplan_model: WorkPlan, proyect_entity: ProjectEntity) -> WorkplanEntity:
        if workplan_model is None:
            return None
        activities_entity = [self.activity_service.activity_to_entity(activity_model)
        for activity_model in workplan_model.activities
        ] if workplan_model.activities else []
        return WorkplanEntity(
            id= workplan_model.id,
            description= workplan_model.description,
            duration_estimate=workplan_model.duration_estimate,
            activities=activities_entity,
            project=proyect_entity
        )

    #mandar notificacion al alcanzar un porcentaje completo 