import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.app import app, activities

client = TestClient(app)

def test_root_redirect():
    """Test if the root URL redirects to the static index.html"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Mergington High School" in response.text

def test_get_activities():
    """Test if the /activities endpoint returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    assert response.json() == activities

def test_signup_for_activity():
    """Test signing up a student for an activity"""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]

def test_signup_already_registered():
    """Test signing up a student who is already registered"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json() == {"detail": "Already signed up"}

def test_signup_activity_not_found():
    """Test signing up for a non-existent activity"""
    activity_name = "NonExistentActivity"
    email = "student@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_cancel_signup():
    """Test canceling a student's signup for an activity"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/{activity_name}/cancel", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Canceled signup for {email} in {activity_name}"}
    assert email not in activities[activity_name]["participants"]

def test_cancel_signup_not_registered():
    """Test canceling a signup for a student who is not registered"""
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    response = client.delete(f"/activities/{activity_name}/cancel", params={"email": email})
    assert response.status_code == 400
    assert response.json() == {"detail": "Student not signed up for this activity"}

def test_cancel_signup_activity_not_found():
    """Test canceling a signup for a non-existent activity"""
    activity_name = "NonExistentActivity"
    email = "student@mergington.edu"
    response = client.delete(f"/activities/{activity_name}/cancel", params={"email": email})
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}