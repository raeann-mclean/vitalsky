from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://telemed:telemed@localhost:5432/telemed"
    ai_provider: str = "mock"
    aws_region: str = "us-east-1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
