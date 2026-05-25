"""Application configuration loaded from .env file."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All app config in one place. Values come from .env."""

    aws_region: str
    s3_bucket_name: str
    max_upload_size_mb: int = 10
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# Single instance everyone else imports
settings = Settings()