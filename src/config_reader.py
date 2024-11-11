from pydantic import SecretStr, computed_field, PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    debug: bool
    bot_token: SecretStr
    timezone: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    postgres_port: int
    notion_api_key: SecretStr
    notion_db_id: SecretStr

    @computed_field
    @property
    def database_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host if not self.debug else "localhost",
            port=self.postgres_port if not self.debug else 5435,
            path=self.postgres_db,
        )


settings = Settings()
