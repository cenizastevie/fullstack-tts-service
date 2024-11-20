import os
import sys
from datetime import datetime
from io import BytesIO

import boto3
import numpy as np
import requests
from PIL import Image
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest

from app.main import app
from app.config import settings
from app.database import get_db
from app.models import Base, ImageMetadata

sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

client = TestClient(app)

@pytest.fixture(scope="module")
def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint
    )

@pytest.fixture(scope="module")
def db_session():
    engine = create_engine(settings.database_url)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def bucket_exists(s3_client, bucket_name):
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return bucket_name in buckets

def test_bucket_exists(s3_client):
    """Test if the S3 bucket exists."""
    assert bucket_exists(s3_client, settings.image_bucket)

def test_image_service_health_check():
    """Test the health check endpoint of the image service."""
    response = client.get("/v1/image-service/health-check")
    assert response.status_code == 200

def test_get_presigned_url_valid_fields():
    """Test getting a presigned URL with valid fields."""
    response = client.post("/v1/image-service/presigned-url", json={
        "file_name": "test.jpeg",
        "date": "2023-01-01",
        "patient_id": "12345",
        "source_id": "hospital_1",
        "diagnosis": "normal"
    })
    assert response.status_code == 200
    json_response = response.json()
    assert "presigned_url" in json_response
    assert "metadata" in json_response
    assert json_response["metadata"]["date"] == "2023-01-01"
    assert json_response["metadata"]["patient_id"] == "12345"
    assert json_response["metadata"]["source_id"] == "hospital_1"
    assert json_response["metadata"]["diagnosis"] == "normal"

def test_get_presigned_url_missing_metadata():
    """Test getting a presigned URL with missing metadata."""
    response = client.post("/v1/image-service/presigned-url", json={})
    assert response.status_code != 200

def test_upload_image_all_metadata():
    """Test uploading an image with all metadata."""
    response = client.post("/v1/image-service/upload", json={
        "file_name": "test.jpeg",
        "date": "2023-01-01",
        "patient_id": "12345",
        "source_id": "hospital_1",
        "diagnosis": "normal"
    })
    assert response.status_code == 200
    json_response = response.json()
    assert "presigned_url" in json_response
    assert "metadata" in json_response
    assert "date" in json_response["metadata"]
    assert "patient_id" in json_response["metadata"]
    assert "source_id" in json_response["metadata"]
    assert "diagnosis" in json_response["metadata"]

def test_presigned_image_presigned_url(s3_client):
    """Test uploading an image using a presigned URL."""
    response = client.post("/v1/image-service/presigned-url", json={
        "date": "2023-01-01",
        "patient_id": "12345",
        "source_id": "hospital_1",
        "diagnosis": "normal"
    })
    assert response.status_code == 200
    presigned_url_data = response.json()

    file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'test.jpeg')
    files = {'file': open(file_path, 'rb')}
    response = requests.post(presigned_url_data['url'], data=presigned_url_data['fields'], files=files)
    assert response.status_code == 204
    
    # Verify the file is in the S3 bucket
    response = s3_client.list_objects_v2(Bucket=settings.image_bucket)
    assert 'Contents' in response
    filenames = [obj['Key'] for obj in response['Contents']]
    assert "test.jpeg" in filenames

def test_image_preprocessing(s3_client, db_session):
    """Test the image preprocessing functionality."""
    file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'test.jpeg')
    s3_client.put_object(
        Bucket=settings.image_bucket,
        Key="test.jpeg",
        Body=open(file_path, 'rb'),
        Metadata={
            "date": "2023-01-01",
            "patient_id": "12345",
            "source_id": "hospital_1",
            "diagnosis": "normal"
        }
    )

    response = client.post("/v1/image-service/preprocess-image", json={"file_name": "test.jpeg"})
    assert response.status_code == 200

    response = s3_client.list_objects_v2(Bucket=settings.preprocessed_image_bucket)
    assert 'Contents' in response
    filenames = [obj['Key'] for obj in response['Contents']]
    assert "test.jpeg" in filenames

    db_metadata = db_session.query(ImageMetadata).filter_by(filename="test.jpeg").first()
    assert db_metadata is not None
    assert db_metadata.date == datetime.strptime("2023-01-01", "%Y-%m-%d")
    assert db_metadata.patient_id == "12345"
    assert db_metadata.source_id == "hospital_1"
    assert db_metadata.diagnosis == "normal"

    response = s3_client.get_object(Bucket=settings.preprocessed_image_bucket, Key="test.jpeg")
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