
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.notification_model import Base
from services.notification_service import NotificationService
from models.notification_model import Notifications

# ---------- Test DB Setup -----------

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

# ---------- Tests --------------------------

def test_create_notification(db_session):
    service = NotificationService(db_session)

    notif = service.notify(
        user_id=1,
        message="Task completed."
    )

    assert notif.id is not None
    assert notif.user_id == 1
    assert notif.message == "Task completed."
    assert notif.read is False

def test_get_notifications(db_session):
    service = NotificationService(db_session)

    service.notify(user_id=2, message="Message 1")
    service.notify(user_id=2, message="Message 2")
    service.notify(user_id=3, message="Other user")

    notifs = service.get(user_id=2)
    assert len(notifs) == 2
    assert all(n.user_id == 2 for n in notifs)

def test_mark_as_read(db_session):
    service = NotificationService(db_session)

    notif = service.notify(user_id=4, message="Notification to read")
    service.read(notif.id)

    result = result = db_session.get(Notifications, notif.id)
    assert result.read is True
