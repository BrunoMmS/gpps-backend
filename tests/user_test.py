from main import app
from fastapi.testclient import TestClient

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
def test_empty_fields():
     response = client.post("/users/register", json = {
         "username": "",
         "lastname": "",
          "email": "",
          "password": "",
          "role": ""
        })
     assert response.status_code != 200

def test_invalid_email_format():
     response = client.post("/users/register", json={
         "username": "testuser",
          "lastname": "test",
          "email": "invalid-email",
         "password": "securepassword123",
          "role": "user"
        })
     assert response.status_code != 200

def test_invalid_role():
      response = client.post("users/register", json = {
            "username": "testuser",
            "lastname": "Test",
            "role": "invalid_role",
      })
      assert response.status_code != 200

def user_register_for_login(username, lastname, email, password, role):
      response = client.post("/users/register", json={
         "username": username,
         "lastname": lastname,
         "email": email,
         "password": password,
         "role": role
        })
      
def test_login_success():
      test_email = "test@example.com"
      test_password = "securepassword123"

      user_register_for_login(
            username = "testuser",
            lastname = "Test",
            email = test_email,
            password = test_password,
            role = "user"
      )
      response = client.post("users/login", json = {
            "email": "test@example.com",
            "password" : "securepassword123"
      })
      assert response.status_code == 200

def test_login_invalid_credentials():  
    user_register_for_login("testuser", "Test", "test@ecample.com", "securepassword123", "user")
    response = client.post("/users/login", json = {
            "email": "wrong@example.com",
            "password": "wrongpassword"
      })
    assert response.status_code != 200

def test_login_empty_fields():
    user_register_for_login("testuser", "Test", "test@ecample.com", "securepassword123", "user")
    response = client.post("/users/login", json = {
            "email": "",
            "password": ""
      })
    assert response.status_code != 200

