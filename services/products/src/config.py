from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: str
    DATABASE_URL: str
    RABBIT_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str
    MINIO_PUBLIC_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()