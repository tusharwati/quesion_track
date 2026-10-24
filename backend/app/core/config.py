from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Speech-to-Text Configuration
    stt_model: str = "base"
    stt_device: str = "cpu"
    stt_compute_type: str = "int8"
    
    # Database
    database_url: str = "sqlite:///./data/questiontrack.db"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Frontend
    frontend_url: str = "http://localhost:5173"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Audio Processing
    max_audio_file_size: int = 52428800  # 50MB
    upload_dir: str = "./uploads"
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
