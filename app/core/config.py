from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Сервис пожертвований для котиков"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    INT_DEFAULT_VALUE: int = 0
    STRING_LENGTH: int = 100

    class Config:
        env_file = ".env"


settings = Settings()
