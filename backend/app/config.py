from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AssetFlow API"
    DATABASE_URL: str = "sqlite:///./assetflow.db"

    class Config:
        env_file = ".env"


settings = Settings()