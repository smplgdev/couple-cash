from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: str
    timezone: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int
    notion_api_key: SecretStr
    notion_db_id: SecretStr

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


config = Settings()
