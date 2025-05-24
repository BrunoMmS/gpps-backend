from cruds import notificationDAO
from sqlalchemy.orm import Session

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def notify(self, user_id: int, message: str):
        return notificationDAO.create_notification(self.db, user_id, message)

    def get(self, user_id: int, no_leidas=False):
        return notificationDAO.get_notifications(self.db, user_id, solo_no_leidas=no_leidas)

    def read(self, notif_id: int):
        return notificationDAO.mark_as_read(self.db, notif_id)
