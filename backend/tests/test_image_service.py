from fastapi.testclient import TestClient

import boto3
import os
import sys
import requests
from PIL import Image
import numpy as np
from io import BytesIO
sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

from app.main import app
from app.config import settings

client = TestClient(app)

def test_image_service_health_check():
    response = client.get("/v1/image-service/health-check")
    assert response.status_code == 200

def test_get_presigned_url():
    response = client.post("/v1/image-service/presigned-url", json={"filename": "test_image.jpg"})
    assert response.status_code == 200
    json_response = response.json()
    assert "url" in json_response
    assert "fields" in json_response

def test_get_presigned_url_missing_filename():
    response = client.post("/v1/image-service/presigned-url", json={})
    assert response.status_code == 422  # Unprocessable Entity
    json_response = response.json()
    assert json_response["detail"][0]["msg"] == "Field required"
    assert json_response["detail"][0]["type"] == "missing"

def test_get_presigned_url_invalid_filename():
    response = client.post("/v1/image-service/presigned-url", json={"filename": ""})
    assert response.status_code == 422  # Unprocessable Entity
    json_response = response.json() 
    assert json_response["detail"][0]["msg"] == "String should have at least 5 characters"
    assert json_response["detail"][0]["type"] == "string_too_short"

def test_upload_file_to_presigned_url():
    # Step 1: Generate the presigned URL
    response = client.post("/v1/image-service/presigned-url", json={"filename": "test_image.jpg"})
    assert response.status_code == 200
    presigned_url_data = response.json()
    print(presigned_url_data)
    # Step 2: Upload the file using the presigned URL
    file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'test_image.jpg')
    files = {'file': open(file_path, 'rb')}
    response = requests.post(presigned_url_data['url'], data=presigned_url_data['fields'], files=files)
    # Check if the file upload was successful
    assert response.status_code == 204
    
    # Step 3: Verify the file is in the S3 bucket
    s3_client = boto3.client(
        "s3",
        endpoint_url=f"http://{os.getenv('LOCALSTACK_HOSTNAME')}:{os.getenv('LOCALSTACK_PORT')}"
    )
    response = s3_client.list_objects_v2(Bucket=settings.image_bucket)
    assert 'Contents' in response
    filenames = [obj['Key'] for obj in response['Contents']]
    assert "test_image.jpg" in filenames

    # Step 4: Download the image from S3 and verify preprocessing
    response = s3_client.get_object(Bucket=settings.image_bucket, Key="test_image.jpg")
    image_data = response['Body'].read()
    image = Image.open(BytesIO(image_data))

    # Verify the image is grayscale
    assert image.mode == "L"

    # Verify the image dimensions
    assert image.size == (256, 256)

    # Verify the pixel value range
    image_np = np.array(image)
    assert image_np.min() >= 0
    assert image_np.max() <= 255

def test_upload_image_with_metadata():
    file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'test_image.jpg')
    with open(file_path, 'rb') as file:
        response = client.post(
            "/v1/image-service/upload",
            files={"file": file},
            data={
                "date": "2023-01-01",
                "patient_id": "12345",
                "source_id": "hospital_1",
                "diagnosis": "normal"
            }
        )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "file uploaded successfully"
    
    # Verify the file is in the S3 bucket with the correct metadata
    s3_client = boto3.client(
        "s3",
        endpoint_url=f"http://{os.getenv('LOCALSTACK_HOSTNAME')}:{os.getenv('LOCALSTACK_PORT')}"
    )
    response = s3_client.head_object(Bucket=settings.image_bucket, Key="test_image.jpg")
    metadata = response["Metadata"]
    assert metadata["date"] == "2023-01-01"
    assert metadata["patient_id"] == "12345"
    assert metadata["source_id"] == "hospital_1"
    assert metadata["diagnosis"] == "normal"