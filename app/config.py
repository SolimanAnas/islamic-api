from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class Settings(BaseSettings):
    APP_NAME: str = "Islamic API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Free Islamic Data API providing Quran text, Hadith collections, "
        "Hisn Muslim adhkar, duas, tafsir, prayer times, and audio resources. "
        "All data is sourced from authenticated Islamic references."
    )
    APP_URL: str = "https://islamic-api.fly.dev"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    CORS_ORIGINS: list[str] = ["*"]

    RATE_LIMIT: int = 100
    RATE_LIMIT_WINDOW: int = 60

    TAFSIR_DIR: str = str(DATA_DIR / "tafsir")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
