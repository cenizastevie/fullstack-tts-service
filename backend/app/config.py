from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str

    class Config:
        env_file = ".env"

settings = Settings()
audio_bucket = f"tts-service-{settings.environment}-audio"
pdf_bucket = f"tts-service-{settings.environment}-pdf"
text_bucket = f"tts-service-{settings.environment}-text"