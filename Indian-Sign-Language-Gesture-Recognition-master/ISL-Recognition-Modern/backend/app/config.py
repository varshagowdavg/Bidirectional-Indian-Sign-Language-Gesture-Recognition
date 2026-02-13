"""
Configuration settings for the ISL Recognition application.
Uses pydantic-settings for environment variable management.
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application Info
    app_name: str = "ISL Recognition System"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./isl_recognition.db"
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Email Configuration
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""
    
    # File Paths
    model_path: str = "../models"
    data_path: str = "../data"
    
    # File Upload Settings
    max_upload_size: int = 10485760  # 10MB
    allowed_audio_formats: str = "wav,mp3,ogg,m4a"
    allowed_image_formats: str = "jpg,jpeg,png"
    
    # Gesture Recognition Settings
    gesture_confidence_threshold: float = 0.7
    hand_detection_confidence: float = 0.5
    hand_tracking_confidence: float = 0.5
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert comma-separated origins to list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def allowed_audio_formats_list(self) -> List[str]:
        """Convert comma-separated audio formats to list."""
        return [fmt.strip() for fmt in self.allowed_audio_formats.split(",")]
    
    @property
    def allowed_image_formats_list(self) -> List[str]:
        """Convert comma-separated image formats to list."""
        return [fmt.strip() for fmt in self.allowed_image_formats.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid reading .env file multiple times.
    """
    return Settings()
