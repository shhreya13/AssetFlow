from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AssetFlow API"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./assetflow.db"

    # JWT auth
    SECRET_KEY: str = "dev-secret-change-me"  # override via .env in real use
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h — generous for a demo

    class Config:
        env_file = ".env"


settings = Settings()
