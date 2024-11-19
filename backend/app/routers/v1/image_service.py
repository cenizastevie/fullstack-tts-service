from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db  # Import get_db from database.py
from app.models import ImageMetadata
from app.utils.preprocessing import preprocess_image  # Import the preprocessing function
import boto3
import os
from datetime import datetime
from app.config import settings

router = APIRouter()

@router.get("/image-service/health-check")
def health_check():
    return {"message": "Image service is running"}

@router.post("/image-service/upload")
async def upload_image(
    file: UploadFile = File(...),
    date: str = Form(...),
    patient_id: str = Form(...),
    source_id: str = Form(...),
    diagnosis: str = Form(...),
    db: Session = Depends(get_db)
):
    # Preprocess the image
    file_content = await file.read()
    preprocessed_image = preprocess_image(file_content)
    
    # Directly upload the preprocessed image to S3
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint
    )
    s3_client.put_object(
        Bucket=settings.image_bucket,
        Key=file.filename,
        Body=preprocessed_image,
        Metadata={
            "date": date,
            "patient_id": patient_id,
            "source_id": source_id,
            "diagnosis": diagnosis
        }
    )
    
    # Save metadata to the database
    metadata = ImageMetadata(
        filename=file.filename,
        date=datetime.strptime(date, "%Y-%m-%d"),
        patient_id=patient_id,
        source_id=source_id,
        diagnosis=diagnosis
    )
    db.add(metadata)
    db.commit()
    db.refresh(metadata)

    return {"status": "file uploaded successfully"}