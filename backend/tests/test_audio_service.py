from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

from app.main import app

client = TestClient(app)

def test_audio_service_health_check():
    response = client.get("/v1/audio-service/health-check")
    assert response.status_code == 200

def test_get_presigned_url():
    response = client.post("/v1/audio-service/presigned-url", json={"filename": "test_audio.mp3"})
    assert response.status_code == 200
    json_response = response.json()
    assert "url" in json_response
    assert "fields" in json_response

def test_get_presigned_url_missing_filename():
    response = client.post("/v1/audio-service/presigned-url", json={})
    assert response.status_code == 422  # Unprocessable Entity
    json_response = response.json()
    assert json_response["detail"][0]["msg"] == "Field required"
    assert json_response["detail"][0]["type"] == "missing"

def test_get_presigned_url_invalid_filename():
    response = client.post("/v1/audio-service/presigned-url", json={"filename": ""})
    assert response.status_code == 422  # Unprocessable Entity
    json_response = response.json() 
    assert json_response["detail"][0]["msg"] == "String should have at least 5 characters"
    assert json_response["detail"][0]["type"] == "string_too_short"