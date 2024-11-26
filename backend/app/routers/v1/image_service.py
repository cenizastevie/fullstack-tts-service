from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, get_db_session
from models import ImageMetadata
from utils.preprocessing import preprocess_image
from datetime import datetime
from config import settings
from pydantic import BaseModel

import boto3
import os
import logging
import tempfile
import traceback

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
router = APIRouter()

class PresignedUrlRequest(BaseModel):
    file_name: str
    date: str
    patient_id: str
    source_id: str
    diagnosis: str

@router.get("/image-service/health-check")
def health_check():
    return {"message": "Image service is running"}

@router.post("/image-service/presigned-url")
def generate_presigned_url(request: PresignedUrlRequest):
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint
    )
    try:
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.image_bucket,
                'Key': request.file_name,
                'Metadata': {
                    'date': request.date,
                    'patient_id': request.patient_id,
                    'source_id': request.source_id,
                    'diagnosis': request.diagnosis
                }
            },
            ExpiresIn=3600  # URL expiration time in seconds
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not generate presigned URL: {str(e)}")

    return {
        "presigned_url": presigned_url,
        "metadata": {
            "date": request.date,
            "patient_id": request.patient_id,
            "source_id": request.source_id,
            "diagnosis": request.diagnosis
        }
    }

@router.post("/image-service/metadata")
def save_metadata(data: dict, db: Session = Depends(get_db)):
    # Use the session provided by FastAPI's dependency injection
    image_metadata = ImageMetadata(**data)
    db.add(image_metadata)
    db.commit()
    return {"message": "Metadata saved successfully"}

def preprocess_image_and_save(file_name: str):
    try:
        s3_client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            local_file_path = os.path.join(temp_dir, file_name)
            processed_file_path = os.path.join(temp_dir, f"processed_{file_name}")

            s3_client.download_file(settings.image_bucket, file_name, local_file_path)
            logging.info(f"Downloaded image {file_name} from S3 to {local_file_path}")

            with open(local_file_path, "rb") as image_file:
                image_bytes = image_file.read()
            logging.info(f"Read image {file_name} as bytes")

            # Retrieve metadata from S3
            image_metadata = s3_client.head_object(Bucket=settings.image_bucket, Key=file_name)
            metadata = {
                "date": image_metadata["Metadata"]["date"],
                "patient_id": image_metadata["Metadata"]["patient_id"],
                "source_id": image_metadata["Metadata"]["source_id"],
                "diagnosis": image_metadata["Metadata"]["diagnosis"],
                "file_name": file_name
            }

            with get_db_session() as db:
                image_metadata_db = ImageMetadata(**metadata)
                db.add(image_metadata_db)
                db.commit()

            new_image_bytes = preprocess_image(image_bytes)
            with open(processed_file_path, "wb") as new_image_file:
                new_image_file.write(new_image_bytes)
            logging.info(f"Processed image saved as {processed_file_path}")
            processed_file_name = f"processed_{file_name}"
            s3_client.upload_file(processed_file_path, settings.preprocessed_image_bucket, processed_file_name)
            logging.info(f"Uploaded processed image {processed_file_path} to S3")

            return True, None
    except Exception as e:
        logging.error(f"An error occurred during image preprocessing: {str(e)}")
        traceback.print_exc()
        return False, str(e)