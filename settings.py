from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    bot_token: str
    openai_key: str
    assistant_key: str
    async_db_url: str
    amplitude_api_key: str
    redis_storage_url: str


setting = Settings()
