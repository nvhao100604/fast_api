from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CV Evaluator API"
    API_V1_STR: str = "/api/v1"
    MODEL_NAME: str = "all-MiniLM-L6-v2"  # Quản lý tên model tại đây
    
    class Config:
        env_file = ".env"

settings = Settings()
