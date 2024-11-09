from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr
from config import settings
import boto3
from botocore.exceptions import NoCredentialsError

router = APIRouter()

class PresignedUrlRequest(BaseModel):
    filename: constr(min_length=5)

@router.get("/audio-service/health-check")
def audio_service():
    return {"message": "Audio service is running"}

@router.post("/audio-service/presigned-url")
def get_presigned_url(request: PresignedUrlRequest):
    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_post(
            Bucket=settings.audio_bucket,
            Key=request.filename,
            Fields=None,
            Conditions=None,
            ExpiresIn=3600,
        )
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="AWS credentials not found")
    return response