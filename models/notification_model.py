from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base
from db.db import BaseDBModel 

class Notifications(BaseDBModel):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
