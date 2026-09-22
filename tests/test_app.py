from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant():
    email = "newstudent@mergington.edu"
    activity = "Soccer Team"

    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert unregister_response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]

    missing_response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert missing_response.status_code == 400
