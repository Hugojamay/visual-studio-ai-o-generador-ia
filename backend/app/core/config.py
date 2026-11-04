from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "VISUAL STUDIO AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    COMFYUI_HTTP_URL: str = "http://127.0.0.1:8188"
    COMFYUI_WS_URL: str = "ws://127.0.0.1:8188/ws"
    
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./visual_studio_ai.db"
    
    OUTPUT_DIRECTORY: str = "./storage/generations"
    TEMP_DIRECTORY: str = "./storage/temp"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()