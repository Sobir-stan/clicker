from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./clicker.db"
    SECRET_KEY: str = "change-me-later"

    class Config:
        env_file = ".env"


settings = Settings()
