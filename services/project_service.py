from sqlalchemy.orm import Session
from cruds.projectDAO import ProjectDAO
from cruds.workplanDAO import WorkPlanDAO
from cruds.activityDAO import ActivityDAO
from cruds.taskDAO import TaskDAO
from schema.project_schema import ProjectCreate
from schema.workplan_schema import WorkPlanCreate
from schema.activity_schema import ActivitieCreate
from schema.task_schema import Task
from models.project_model import ProjectModel
from services.workplan_service import WorkPlanService


class ProjectService:
    def __init__(self):
        self.project_dao = ProjectDAO()
        self.workplan_dao = WorkPlanDAO()
        self.activity_dao = ActivityDAO()
        self.task_dao = TaskDAO()

    def crear_proyecto_completo(self, db: Session, data: ProjectCreate) -> ProjectModel:
        new_workplan = self.workplan_dao.create(db, WorkPlanCreate())
        for act in data.workplan.activities:
            activity_data = ActivitieCreate(
                name=act.name,
                duration=act.duration,
                workplan_id=new_workplan.id
            )
            self.activitie_dao.create(db, activity_data)

        for task in data.workplan.activities.tasks:
            task_data = Task(
                description=task.description,
                activity_id=task.activity_id
            )
            self.task_dao.create(db, task_data)

        project_data_dict = data.dict()
        project_data_dict["workplan_id"] = new_workplan.id
        return self.project_dao.create(db, ProjectCreate(**project_data_dict))

    def create_project(self, db: Session, project_data: ProjectCreate) -> ProjectModel:
        return self.project_dao.create(db, project_data)
    
    def add_workplan(self, db: Session,  workplan_data: WorkPlanCreate):
        workplan_service = WorkPlanService()
        return workplan_service.create_workplan(db,  workplan_data)