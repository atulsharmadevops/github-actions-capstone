import json
from app import app

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "ok"
