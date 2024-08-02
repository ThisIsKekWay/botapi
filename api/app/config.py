from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    REDIS_HOST: str
    REDIS_PORT: str
    MONGO_HOST: str
    MONGO_PORT: str


settings = Settings()
