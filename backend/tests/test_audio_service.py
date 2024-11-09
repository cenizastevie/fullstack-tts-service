from fastapi.testclient import TestClient

import boto3
import os
import sys
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

from app.main import app
from app.config import settings

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

def test_upload_file_to_presigned_url():
    # Step 1: Generate the presigned URL
    response = client.post("/v1/audio-service/presigned-url", json={"filename": "test_audio.mp3"})
    assert response.status_code == 200
    presigned_url_data = response.json()

    # Step 2: Upload the file using the presigned URL
    files = {'file': open('test_files/test_audio.mp3', 'rb')}
    response = requests.post(presigned_url_data['url'], data=presigned_url_data['fields'], files=files)

    # Check if the file upload was successful
    assert response.status_code == 204

    # Step 3: Verify the file is in the S3 bucket
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        endpoint_url=f"http://{os.getenv('LOCALSTACK_HOSTNAME')}:{os.getenv('LOCALSTACK_PORT')}"
    )
    response = s3_client.list_objects_v2(Bucket=settings.audio_bucket)
    assert 'Contents' in response
    filenames = [obj['Key'] for obj in response['Contents']]
    assert "test_audio.mp3" in filenames