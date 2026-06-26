"""Environment-backed settings — no secrets committed; use .env locally."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ProspectPilot Platform"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    debug: bool = False
    memory_db_path: str = "data/memory.db"


settings = Settings()
