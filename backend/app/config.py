from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    data_dir: Path = Path("./data")
    library_dir: Path = Path("./sample-library")
    frontend_dist: Path = Path("./static")

    @field_validator("data_dir", "library_dir", "frontend_dist", mode="after")
    @classmethod
    def resolve_relative_path(cls, path: Path) -> Path:
        if path.is_absolute():
            return path

        return (BACKEND_DIR / path).resolve()

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_prefix="ASTRO_LIBRARY_",
    )


settings = Settings()
