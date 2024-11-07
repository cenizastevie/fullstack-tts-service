from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

from app.main import app

client = TestClient(app)

def test_audio_service_cors_options():
    response = client.options("/v1/audio-service")
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"

def test_get_presigned_url():
    response = client.post("/v1/audio-service/presigned-url", json={"filename": "test_audio.mp3"})
    assert response.status_code == 200
    json_response = response.json()
    print(json_response)
    assert "url" in json_response
    assert "fields" in json_response

def test_get_presigned_url_missing_filename():
    response = client.post("/v1/audio-service/presigned-url", json={})
    assert response.status_code == 422  # Unprocessable Entity
    json_response = response.json()
    assert json_response["detail"][0]["msg"] == "field required"
    assert json_response["detail"][0]["type"] == "value_error.missing"

def test_get_presigned_url_invalid_filename():
    response = client.post("/v1/audio-service/presigned-url", json={"filename": ""})
    assert response.status_code == 422  # Unprocessable Entity
    json_response = response.json()
    assert json_response["detail"][0]["msg"] == "ensure this value has at least 1 characters"
    assert json_response["detail"][0]["type"] == "value_error.any_str.min_length"