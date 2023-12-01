from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DSN: PostgresDsn
    DB_ECHO: bool = False
    SALT: str
    ENVIRONMENT: str = "PROD"

    class Config:
        env_file = ".env"


settings = Settings()
