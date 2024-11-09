from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str
    s3_endpoint: str
    
    class Config:
        env_file = ".env"

    @property
    def audio_bucket(self):
        return f"tts-service-{self.environment}-audio"

    @property
    def pdf_bucket(self):
        return f"tts-service-{self.environment}-pdf"

    @property
    def text_bucket(self):
        return f"tts-service-{self.environment}-text"

settings = Settings()