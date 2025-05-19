from sqlalchemy.orm import Session
from cruds.proyectPPSDAO import ProyectDAO
from cruds.workplanDAO import WorkPlanDAO
from cruds.activitiesDAO import ActivitiesDAO
from cruds.tasksDAO import tasksDAO
from schema.proyectPPS_schema import ProyectCreate
from schema.workplan_schema import WorkPlanCreate
from schema.activities_schema import ActivitiesCreate
from schema.tasks_schema import TaskCreate  
from models.proyectPPS_model import ProyectPPS


class ProyectService:
    def __init__(self):
        self.proyect_dao = ProyectDAO()
        self.workplan_dao = WorkPlanDAO()
        self.activities_dao = ActivitiesDAO()
        self.tasks_dao = tasksDAO()

    def crear_proyecto_completo(self, db: Session, data: ProyectCreate) -> ProyectPPS:
        new_workplan = self.workplan_dao.create(db, WorkPlanCreate())
        for act in data.workplan.activities:
            activity_data = ActivitiesCreate(
                name=act.name,
                duration=act.duration,
                workplan_id=new_workplan.id
            )
            self.activities_dao.create(db, activity_data)

        for task in data.workplan.activities.tasks:
            task_data = TaskCreate(
                description=task.description,
                activity_id=task.activity_id
            )
            self.tasks_dao.create(db, task_data)

        proyect_data_dict = data.dict()
        proyect_data_dict["workplan_id"] = new_workplan.id
        return self.proyect_dao.create(db, ProyectCreate(**proyect_data_dict))
