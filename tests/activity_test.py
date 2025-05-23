from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

idWorkplan : int = 1

def test_create_activity_success():
    response = client.post("activity/create?workplan_id={idWorkplan}", json = {
        "id": 0,
        "duration": 100,
        "name": "Test Activity",
        "done": False,
        "workplan_id": 1
    })
    assert response.status_code == 200

def test_create_activity_invalid_workplan():
    response = client.post("activity/create?workplan_id={idWorkplan}", json = {
        "id": 0,
        "duration": 100,
        "name": "Test Activity",
        "done": False,
        "workplan_id": 9999
    })
    assert response.status_code != 200

def test_create_activity_empty_fields():
    response = client.post("activity/create?workplan_id={idWorkplan}", json = {
        "id": 0,
        "duration": 100,
        "name": "",
        "workplan_id": 1
    })
    assert response.status_code != 200

def test_create_activity_invalid_duration():
    response = client.post("activity/create?workplan_id={idWorkplan}", json = {
        "id": 0,
        "duration": -10,
        "name": "Test Activity",
        "workplan_id": 1
    })
    assert response.status_code != 200