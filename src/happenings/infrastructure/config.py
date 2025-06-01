"""
Application configuration settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    """

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Happenings"

    # Security
    SECRET_KEY: str = "my_super_secure_key"  # Use environment variable in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./happenings.db"

    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]


settings = Settings()
