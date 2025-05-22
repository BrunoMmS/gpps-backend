from main import app
from fastapi.testclient import TestClient

def test_user():
    client = TestClient(app)

    def test_register_user_success():
        response = client.post("/users/register", json={
            "id": 0, 
            "username": "testuser",
            "lastname": "Test",
            "email": "test@example.com",
            "password": "securepassword123",
            "role":"user"
            
        })
        assert response.status_code == 200 or response.status_code == 201 
        data = response.json()
        assert "username" in data
        assert data["username"] == "testuser"

    def test_existing_user_mail():
        client.post("/users/register", json={
            "username": "user",
            "lastname": "first",
            "email": "existing@example.com",
            "password": "password123",
            "role": "user"
        })

        response = client.post("/users/register", json = {
            "username": "anotheruser",
            "lastname": "Another",
            "email": "existing@example.com",
            "password": "password456",
            "role": "user"
        })

        assert response.status_code != 200
        assert "detail" in response.json()
        assert "Email already registered" in response.json()["detail"]