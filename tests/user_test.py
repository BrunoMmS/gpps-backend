def test_register_user_success(client):
    response = client.post("/users/register", json={
        "id": 0,
        "username": "testuser",
        "lastname": "Test",
        "email": "test@example.com",
        "password": "securepassword123",
        "role": "user"
    })
    assert response.status_code == 200 or response.status_code == 201 
    data = response.json()
    assert "username" in data
    assert data["username"] == "testuser"

def test_existing_user_mail(client):
    client.post("/users/register", json={
      "id": 0,
      "username": "user",
      "lastname": "first",
      "email": "existing@example.com",
      "password": "password123",
      "role": "user"
    })

    response = client.post("/users/register", json={
      "id": 0,
        "username": "anotheruser",
        "lastname": "Another",
        "email": "existing@example.com",
        "password": "password456",
        "role": "user"
    })

    assert response.status_code != 200

def test_empty_fields(client):
    response = client.post("/users/register", json={
      "id": 0,
        "username": "",
        "lastname": "",
        "email": "",
        "password": "",
        "role": ""
    })
    assert response.status_code != 200

def test_invalid_email_format(client):
    response = client.post("/users/register", json={
      "id": 0,
        "username": "testuser",
        "lastname": "test",
        "email": "invalid-email",
        "password": "securepassword123",
        "role": "user"
    })
    assert response.status_code != 200

def test_invalid_role(client):
    response = client.post("/users/register", json={
        "id": 0,
        "username": "testuser",
        "lastname": "Test",
        "email": "testrole@example.com",
        "password": "securepassword123",
        "role": "invalid_role"
    })
    assert response.status_code != 200

def user_register_for_login(username, lastname, email, password, role, client):
    response = client.post("/users/register", json={
      "id": 0,
        "username": username,
        "lastname": lastname,
        "email": email,
        "password": password,
        "role": role
    })

def test_login_success(client):
    test_email = "test@example.com"
    test_password = "securepassword123"

    user_register_for_login(
        username="testuser",
        lastname="Test",
        email=test_email,
        password=test_password,
        role="user",
        client=client
    )

    response = client.post("/users/login", json={
        "email": test_email,
        "password": test_password
    })
    assert response.status_code == 200

def test_login_invalid_credentials(client):
    user_register_for_login(
        "testuser", "Test", "test@example.com", "securepassword123", "user", client
    )

    response = client.post("/users/login", json={
        "email": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code != 200

def test_login_empty_fields(client):
    user_register_for_login(
        "testuser", "Test", "test@example.com", "securepassword123", "user", client
    )

    response = client.post("/users/login", json={
        "email": "",
        "password": ""
    })
    assert response.status_code != 200
