"""
Модуль конфигураций.
"""
import typing

from pydantic import BaseSettings, Field


DOC_OPENAPI = '/openapi.json'


class Database(BaseSettings):
    """
    Класс констант для базы данных.
    """
    pass

    class Config:
        case_sensitive = True


class Settings(BaseSettings):
    """
    Класс настроек сервера.
    """
    PROJECT_NAME: str
    PROJECT_VERSION: str

    SERVER_HOST: str
    SERVER_PORT: int

    WORKERS: int

    TESTING: bool = Field(default=False)

    OPENAPI: bool = Field(default=False)
    ECHO_DB: bool = Field(default=False)

    LOGGER: bool = Field(default=False)
    LOGS_PATH: str = Field(default='logs')
    LOGS_COUNT: int = Field(default=10)

    BACKEND_CORS_ORIGINS: typing.Union[typing.List] = []

    REDIRECT_HTTPS: bool = Field(default=True)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    TEST_API: bool = Field(default=False)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


db_config = Database()
base_config = Settings(_env_file='.env', _env_file_encoding='utf-8')
print(base_config.TEST_API)
