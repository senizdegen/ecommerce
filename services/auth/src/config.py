from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: str
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    RABBIT_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
