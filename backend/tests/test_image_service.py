from fastapi.testclient import TestClient

import boto3
import os
import sys
import requests
from PIL import Image
import numpy as np
from io import BytesIO
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Base, ImageMetadata
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

from app.main import app
from app.config import settings
from app.database import get_db
client = TestClient(app)

# Use settings to get the DATABASE_URL

def bucket_exists(bucket_name):
    s3_client = boto3.client(
        "s3",
        endpoint_url=f"http://{os.getenv('LOCALSTACK_HOSTNAME')}:{os.getenv('LOCALSTACK_PORT')}"
    )
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return bucket_name in buckets

def test_image_service_health_check():
    response = client.get("/v1/image-service/health-check")
    assert response.status_code == 200

def test_upload_image_with_metadata():
    file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'test.jpeg')
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
    response = s3_client.head_object(Bucket=settings.image_bucket, Key="test.jpeg")
    metadata = response["Metadata"]
    assert metadata["date"] == "2023-01-01"
    assert metadata["patient_id"] == "12345"
    assert metadata["source_id"] == "hospital_1"
    assert metadata["diagnosis"] == "normal"

    # Verify the metadata is in the database
    db = next(get_db())
    db_metadata = db.query(ImageMetadata).filter_by(filename="test.jpeg").first()
    assert db_metadata is not None
    assert db_metadata.date == datetime.strptime("2023-01-01", "%Y-%m-%d")
    assert db_metadata.patient_id == "12345"
    assert db_metadata.source_id == "hospital_1"
    assert db_metadata.diagnosis == "normal"

    # Clean up: Delete the file from S3 and the metadata from the database
    s3_client.delete_object(Bucket=settings.image_bucket, Key="test.jpeg")
    db.delete(db_metadata)
    db.commit()
    db.close()

def test_bucket_exists():
    assert bucket_exists(settings.image_bucket)