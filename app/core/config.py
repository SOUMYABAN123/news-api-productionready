from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    GNEWS_API_KEY: str
    GNEWS_LANG: str = "en"
    GNEWS_COUNTRY: str = "us"
    GNEWS_MAX: int = 10

    # REDIS_HOST: str = "redis"
    # REDIS_PORT: int = 6379 

    REDIS_URL: str

    MODEL_VERSION: str = "v1"

settings = Settings()
