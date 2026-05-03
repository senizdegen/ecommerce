from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    CART_SERVICE_URL: str
    INVENTORY_SERVICE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    PRODUCT_SERVICE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

Config = Settings()