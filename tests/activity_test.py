
idWorkplan : int = 1

def test_create_activity_success(client):
    response = client.post(f"activity/create?workplan_id={idWorkplan}", json = {

        "duration": 100,
        "name": "Test Activity",
        "done": False,

    })
    assert response.status_code == 200

def test_create_activity_empty_fields(client):
    response = client.post(f"activity/create?workplan_id={idWorkplan}", json = {
       
        "duration": 100,
        "name": "",
        
    })
    assert response.status_code != 200

def test_create_activity_invalid_duration(client):
    response = client.post(f"activity/create?workplan_id={idWorkplan}", json = {
        
        "duration": -10,
        "name": "Test Activity",
      
    })
    assert response.status_code != 200