from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_signup_and_unregister_participant():
    # Arrange
    activity = "Soccer Team"
    email = "student@mergington.edu"
    activities[activity]["participants"] = []

    # Act
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    participants_after_signup = client.get("/activities").json()[activity]["participants"]

    unregister_response = client.delete(f"/activities/{activity}/participants?email={email}")
    participants_after_unregister = client.get("/activities").json()[activity]["participants"]

    # Assert
    assert signup_response.status_code == 200
    assert email in participants_after_signup

    assert unregister_response.status_code == 200
    assert email not in participants_after_unregister


def test_unregister_missing_participant_returns_400():
    # Arrange
    activity = "Soccer Team"
    email = "missing@mergington.edu"
    activities[activity]["participants"] = []

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
