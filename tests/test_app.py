# tests/test_app.py
import json
import sys
import os

# Add repo root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "ok"

