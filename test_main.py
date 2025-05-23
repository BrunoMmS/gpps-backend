from fastapi.testclient import TestClient
from sqlalchemy import true

from main import app

client = TestClient(app)


def test_create_proyect():
    response = client.post("/projects/create",json={
          "title": "string",
          "description": "string",
          "active": True,
          "start_date": "2025-04-20",
          "user_id": 1,
          "end_date": "2025-05-25"
    })
    assert response.status_code == 200
    
def test_get_proyect():
    response = client.get("/projects/")
    assert response.status_code == 200

def test_get_proyect_by_user():
    idUser= 1
    response = client.get(f"/projects/{idUser}")
    assert response.status_code == 200


def test_assign_user_to_proyect():
    response = client.post(
        "/projects/assignUserToProject",
        params={
            "user_id": 4,
            "project_id": 3,
            "user_to_assign": 1
        }
    )
    assert response.status_code == 200

