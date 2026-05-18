from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "tft-analytics"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://tft_analytics_user:password@localhost:5433/tft_analytics_db"
    jwt_secret_key: str = Field(default="change-me-local-only")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 14
    riot_api_key: str = ""
    riot_default_region: str = "kr"
    riot_default_routing: str = "asia"
    backend_cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]

    @property
    def refresh_cookie_name(self) -> str:
        return "refresh_token"

    @property
    def refresh_cookie_secure(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

