import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    """Test that root path redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_new_participant():
    """Test signing up a new participant"""
    activity = "Chess Club"
    email = "test@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]

def test_signup_duplicate_participant():
    """Test signing up a participant who is already registered"""
    activity = "Chess Club"
    email = "michael@mergington.edu"  # This email is already in the participants list
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]

def test_signup_nonexistent_activity():
    """Test signing up for a non-existent activity"""
    activity = "NonexistentClub"
    email = "test@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]

def test_unregister_participant():
    """Test unregistering a participant"""
    # First, add a test participant
    activity = "Chess Club"
    email = "unregister_test@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Then try to unregister them
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]

def test_unregister_nonregistered_participant():
    """Test unregistering a participant who is not registered"""
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"]