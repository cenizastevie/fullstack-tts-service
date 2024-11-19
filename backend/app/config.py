from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    localstack_hostname: str
    localstack_port: int
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    s3_endpoint: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    environment: str

    class Config:
        env_file = ".env"

    @property
    def image_bucket(self):
        return f"tts-service-{self.environment}-medical-images"
    
    @property
    def database_url(self):
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()