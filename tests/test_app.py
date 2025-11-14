import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Check participant added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]

def test_unregister_from_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]
    # Check participant removed
    get_resp = client.get("/activities")
    assert email not in get_resp.json()[activity]["participants"]

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_invalid_participant():
    response = client.post("/activities/Chess Club/unregister?email=notfound@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
