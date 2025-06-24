"""Configuration settings for the application."""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Claude API
    claude_api_key: str

    # BigQuery
    bq_private_key_id: str
    bq_private_key: str
    bq_client_email: str
    bq_client_id: str
    bq_project_id: str = "growth-force-project"
    bq_dataset_id: str = "semantic"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"

    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]

    # Environment
    environment: str = "development"

    # Timeouts (in seconds)
    claude_timeout: int = 300  # 5 minutes
    bigquery_timeout: int = 120  # 2 minutes
    api_request_timeout: int = 600  # 10 minutes

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    def get_cors_origins(self) -> List[str]:
        """Get CORS origins from comma-separated string."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins


settings = Settings()