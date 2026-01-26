from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "CV Evaluator API"
    API_V1_STR: str = "/api/v1"
    MODEL_NAME: str = "all-MiniLM-L6-v2"  # Quản lý tên model tại đây
    DATABASE_URL: str
    
    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = Settings()
