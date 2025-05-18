from sqlalchemy.orm import Session
from cruds.proyectPPSDAO import proyectPPSDAO
from models.proyectPPS_model import ProyectPPS

class proyectPPSService:
    def __init__(self):
        self.dao = proyectPPSDAO()
    