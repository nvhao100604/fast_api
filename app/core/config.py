from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from functools import lru_cache

class Settings(BaseSettings):    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # --- Security ---
    SECRET_KEY: str = "" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- General ---
    PROJECT_NAME: str
    ENVIRONMENT: str = "development"
    MODEL_NAME: str = "all-MiniLM-L6-v2" 

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

@lru_cache
def get_settings():
    return Settings()

settings = Settings()
