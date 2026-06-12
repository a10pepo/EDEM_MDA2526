from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación leída de variables de entorno / .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Base de datos
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ecommerce"

    # AWS / S3
    aws_region: str = "eu-west-1"
    s3_bucket_name: str = "ecommerce-ropa-media"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    s3_presign_expiration: int = 3600

    # App
    app_env: str = "local"


@lru_cache
def get_settings() -> Settings:
    return Settings()
