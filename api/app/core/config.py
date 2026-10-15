from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    """Application configuration"""
    
    # Application
    APP_NAME: str = "NNY Emergency Dashboard"
    APP_ENV: str = "development"
    
    # Database
    DATABASE_URL: str = Field(default="postgresql://emdash:emdash_secure_password_change_me@localhost:5432/nny_em_dashboard", description="PostgreSQL connection string")
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # JWT
    JWT_SECRET_KEY: str = Field(default="change_this_in_production", description="JWT secret key (change in production)")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list[str] = Field(default=["*"])
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # SDRtrunk
    SDRTRUNK_HOST: str = "localhost"
    SDRTRUNK_PORT: int = 8000
    SDRTRUNK_STREAM_URL: str = "tcp://localhost:8000/stream"
    
    # Transcription
    WHISPER_MODEL: str = "base"
    WHISPER_DEVICE: str = "cpu"
    
    # Celery
    CELERY_BROKER: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

settings = get_settings()
