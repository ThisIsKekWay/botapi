from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    REDIS_HOST: str
    REDIS_PORT: str
    MONGO_HOST: str
    MONGO_PORT: str


    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
