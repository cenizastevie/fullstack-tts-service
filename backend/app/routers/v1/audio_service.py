from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr
from config import settings
import boto3
from botocore.exceptions import NoCredentialsError

router = APIRouter()

class PresignedUrlRequest(BaseModel):
    filename: constr(min_length=5)

@router.get("/audio-service")
def audio_service():
    return {"message": "Audio service is running"}

@router.post("/audio-service/presigned-url")
def get_presigned_url(request: PresignedUrlRequest):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )
    try:
        response = s3_client.generate_presigned_post(
            Bucket=settings.s3_bucket_name,
            Key=request.filename,
            Fields=None,
            Conditions=None,
            ExpiresIn=3600,
        )
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="AWS credentials not found")
    return response