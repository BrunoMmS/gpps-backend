from typing import List
from entities.project_entity import ProjectEntity
from entities.workplan_entity import WorkplanEntity


class ReportEntity:
    def __init__(self, project: ProjectEntity, workplan: WorkplanEntity):
        self.project = project
        self.workplan = workplan

    def generate_lines(self) -> List[str]:
        lines = []
        lines.append(f"Proyecto: {self.project.getTitle()}")
        lines.append(f"Descripción: {self.project.getDescription()}")
        lines.append(f"Activo: {'Sí' if self.project.isActive() else 'No'}")
        lines.append(f"Fecha de inicio: {self.project.getStartDate()}")
        lines.append(f"Fecha de fin: {self.project.getEndDate() or 'No definida'}")
        lines.append("")

        if self.workplan:
            lines.append(f"Workplan:")
            lines.append(f"Descripción: {self.workplan.getDescription()}")
            lines.append(f"Duración estimada: {self.workplan.getDuration()}")
            lines.append(f"Porcentaje de actividades hechas: {self.workplan.get_completed_percent()}")
            lines.append(f"Porcentaje de no actividades hechas: {self.workplan.get_incopmlete_percent()}")
            for activity in self.workplan.getActivities():
                lines.append(f"    - Actividad: {activity.getName()}")
                lines.append(f"      Duración: {activity.getDuration()}")
                lines.append(f"      Completada: {'Sí' if activity.isFinished() else 'No'}")
                lines.append(f"      Porcentaje de tareas hechas: {activity.get_complete_percent()}")
                lines.append(f"      Porcentaje de tareas no hechas: {activity.get_incomplete_percent()}")
                if activity.getJobs():
                    lines.append("      Tareas:")
                    for task in activity.getJobs():
                        lines.append(f"        * {task.getDescription()} - {'Completada' if task.isDone() else 'Pendiente'}")
                else:
                    lines.append("No tiene tareas.")
                lines.append("")
        else:
            lines.append("No hay workplan definido.")
        return lines
