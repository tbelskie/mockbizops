"""Application configuration."""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Application settings."""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/car_repair_api"
    MARKETING_DATABASE_URL: str = "postgresql://user:password@localhost:5432/marketing"

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ADMIN_API_KEY: str = "admin-key-change-in-production"

    # Application
    PROJECT_NAME: str = "Car Repair Shop Mock API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # CORS - accepts comma-separated string or list
    CORS_ORIGINS: Union[List[str], str] = "*"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            # Split comma-separated string
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
