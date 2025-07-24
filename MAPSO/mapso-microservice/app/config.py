import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MAPSO Microservice"
    app_version: str = "2.3"
    debug: bool = False
    max_file_size: int = 1024 * 1024 * 100  # 100MB
    temp_file_dir: str = "./temp_files"
    ocr_enabled: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Create temp directory if it doesn't exist
os.makedirs(settings.temp_file_dir, exist_ok=True)