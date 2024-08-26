import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = None
    DB_PORT: int = None
    DB_NAME: str = None
    DB_USER: str = None
    DB_PASSWORD: str = None
    SECRET_KEY: str = None
    ALGORITHM: str = None
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


"""def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")"""

#"sqlite+aiosqlite:///./auth.db"
def get_db_url():
    return ("sqlite:///./auth.db")

def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}
