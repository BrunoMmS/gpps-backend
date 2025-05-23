
user_id : int = 1

def test_create_workplan_success(client):
    response = client.post(f"/workplan/create?user_id={user_id}", json = {
        "id": 1,
        "project_id": 1,
        "description": "test Workplan",
        "user_id": 1
    })
    assert response.status_code == 200

def test_create_workplan_empty_fields(client):
    response = client.post(f"/workplan/create?user_id={user_id}", json = {
        "id": 1,
        "project_id": "",
        "description": "", 
        "user_id": 1
    })
    assert response.status_code != 200