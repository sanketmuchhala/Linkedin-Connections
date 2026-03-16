"""
Configuration settings for the application.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "sqlite:///data/linkedin_intelligence.db"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Application
    APP_NAME: str = "LinkedIn Network Intelligence"
    APP_VERSION: str = "1.0.0"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins as list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = "backend/.env"
        case_sensitive = True


settings = Settings()
