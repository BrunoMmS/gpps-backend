from sqlalchemy.orm import Session
from cruds.workplanDAO import WorkPlanDAO
from schemas.workplan_schema import WorkPlanCreate
from roles.rol import Rol
from services.user_service import UserService

class WorkPlanService:
    def __init__(self):
        self.workplan_dao = WorkPlanDAO()
        self.user_service = UserService()

    def create_workplan(self, db: Session, user_id: int, workplan_data: WorkPlanCreate) -> WorkPlanCreate:
        user = self.user_service.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        userEntity = self.user_service.to_entity(user)
        if userEntity.getRole() not in [Rol.student, Rol.exteacher]:
            raise ValueError("El usuario no tiene permisos para crear un plan de trabajo")
        
        return self.workplan_dao.create(db, workplan_data)

    #mandar notificacion al alcanzar un porcentaje completo 