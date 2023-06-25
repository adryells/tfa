import os
from random import choice

from loguru import logger
from pydantic import BaseSettings


class AppConfig(BaseSettings):
    CONFIG_NAME: str = 'TEST_DEV'

    DATABASE_URL: str = ''

    TESTING: bool = True

    DEVELOPMENT: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "TFA_"


def get_config() -> AppConfig:
    if os.getenv("TFA_TESTING") == '1':
        logger.info("Pytest: Pytest detected! Setting/mangling the appropriate variables...")

        random_str = "".join([choice("0123456789") for _ in range(10)])

        # Override database name and config name
        os.environ["TFA_DATABASE_URL"] = f'postgresql+psycopg2://tfa:tfa#1234@127.0.0.1:5433/test_{random_str}'

        os.environ["TFA_CONFIG_NAME"] = "TEST"

        os.environ["BTLX_DEVELOPMENT"] = "0"

    return AppConfig()


settings = get_config()
