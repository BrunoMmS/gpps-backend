from models.notification_model import Notifications
from sqlalchemy.orm import Session

def create_notification(db: Session, user_id: int, message: str):
    notif = Notifications(user_id=user_id, message=message)
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

def get_notifications(db: Session, user_id: int, solo_no_leidas=False):
    query = db.query(Notifications).filter_by(user_id=user_id)
    if solo_no_leidas:
        query = query.filter_by(read=False)
    return query.order_by(Notifications.timestamp.desc()).all()

def mark_as_read(db: Session, notif_id: int):
    notif = db.get(Notifications, notif_id) 
    if notif:
        notif.read = True
        db.commit()
    return notif
