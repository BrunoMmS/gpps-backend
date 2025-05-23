
proyectid : int = 1

def test_create_workplan_success(client):
    response = client.post(f"workplan/create?proyect_id={proyectid}", json = {
        "id": 0,
        "project_id": 1,
        "description": "test Workplan",
    })
    assert response.status_code == 200

def test_create_workplan_empty_fields(client):
    response = client.post(f"workplan/create?proyect_id={proyectid}", json = {
        "id": 0,
        "project_id": 1,
        "description": "", 
    })
    assert response.status_code != 200

def test_create_workplan_invalid_proyect(client):
    response = client.post(f"workplan/create?proyect_id={proyectid}", json = {
        "id": 0,
        "project_id": 999999,
        "description": "Test Workplan"
    })
    assert response.status_code != 200

def test_create_workplan_equals_id(client):
    client.post(f"workplan/create?proyect_id={proyectid}", json = {
        "id": 0,
        "project_id": 1,
        "description": "test Workplan"
    })
    response = client.post(f"workplan/create?proyect_id={proyectid}", json = {
        "id": 0,
        "project_id": 1,
        "description": "test Workplan"
    })
    assert response.status_code != 200