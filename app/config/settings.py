from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    database_url: str

    llm_provider: str = "openai"
    openai_api_key: str | None = None
    llm_model: str = "gpt-4o-mini"
    llm_dummy: bool = False

    otel_service_name: str = "ai-incident-investigation-assistant"
    otel_exporter_otlp_endpoint: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache

def get_settings() -> Settings:
    return Settings()
