from fastapi import APIRouter, Depends, HTTPException
from pytest import Session

from db.db import SessionLocal
from services.notification_service import NotificationService

notification_router = APIRouter(prefix="/notification", tags=["notification"])

def get_db():
    db = SessionLocal()
    try:
        yield db    
    finally:
        db.close()
        
@notification_router.get("/{user_id}")
def get_notifications(user_id: int, db: Session = Depends(get_db)):
    notification_service = NotificationService(db)
    try:
        notifications = notification_service.get(user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return notifications

@notification_router.post("/read/{notif_id}")
def mark_as_read(notif_id: int, db: Session = Depends(get_db)):
    notification_service = NotificationService(db)

    try:
        notification_service.read(notif_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Notificación leida."}

@notification_router.post("/notify/{user_id}")
def notify_user(user_id: int, db: Session = Depends(get_db)):
    notification_service = NotificationService(db)

    try:
        notification_service.notify(user_id=user_id, message="Notificación de prueba")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Notificación leida."}