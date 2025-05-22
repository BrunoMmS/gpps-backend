from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

proyectid : int = 1

def test_create_workplan_success():
    response = client.post("workplan/create?proyect_id={proyectid}", json = {
        "id": 0,
        "project_id": 1,
        "description": "test Workplan",
    })
    assert response.status_code == 200

def test_create_workplan_empty_fields():
    response = client.post("workplan/create?proyect_id={proyectid}", json = {
        "id": 0,
        "project_id": 1,
        "description": "", 
    })
    assert response.status_code != 200

def test_create_workplan_invalid_proyect():
    response = client.post("workplan/create?proyect_id={proyectid}", json = {
        "id": 0,
        "project_id": 999999,
        "description": "Test Workplan"
    })
    assert response.status_code != 200

def test_create_workplan_equals_id():
    client.post("workplan/create?proyect_id={proyectid}", json = {
        "id": 0,
        "project_id": 1,
        "description": "test Workplan"
    })
    response = client.post("workplan/create?proyect_id={proyectid}", json = {
        "id": 0,
        "project_id": 1,
        "description": "test Workplan"
    })
    assert response.status_code != 200