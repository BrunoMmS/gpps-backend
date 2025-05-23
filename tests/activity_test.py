
idWorkplan : int = 1

def test_create_activity_success(client):
    response = client.post(f"activity/create?workplan_id={idWorkplan}", json = {
        "id": 0,
        "duration": 100,
        "name": "Test Activity",
        "done": False,
        "workplan_id": 1
    })
    assert response.status_code == 200

def test_create_activity_invalid_workplan(client):
    response = client.post(f"activity/create?workplan_id={idWorkplan}", json = {
        "id": 0,
        "duration": 100,
        "name": "Test Activity",
        "done": False,
        "workplan_id": 9999
    })
    assert response.status_code != 200

def test_create_activity_empty_fields(client):
    response = client.post(f"activity/create?workplan_id={idWorkplan}", json = {
        "id": 0,
        "duration": 100,
        "name": "",
        "workplan_id": 1
    })
    assert response.status_code != 200

def test_create_activity_invalid_duration(client):
    response = client.post(f"activity/create?workplan_id={idWorkplan}", json = {
        "id": 0,
        "duration": -10,
        "name": "Test Activity",
        "workplan_id": 1
    })
    assert response.status_code != 200