import os
from random import choice

from dotenv import load_dotenv
from loguru import logger
from pydantic.v1 import BaseSettings


class AppConfig(BaseSettings):
    CONFIG_NAME: str = 'TEST_DEV'

    DATABASE_URL: str = ''

    TESTING: bool = True

    DEVELOPMENT: bool = False

    MAL_CLIENT_ID: str = ""

    MAL_CLIENT_SECRET: str = ""

    MAL_BASE_URL: str = ""

    class Config:
        env_file = ".env"
        env_prefix = "TFA_"


def get_config() -> AppConfig:
    load_dotenv()

    if os.getenv("TFA_TESTING") == '1':
        logger.info("Pytest detected! Setting the appropriate variables...")

        random_str = "".join([choice("0123456789") for _ in range(6)])

        # Override database name and config name
        os.environ["TFA_DATABASE_URL"] = f'postgresql+psycopg2://tfa:tfa#123@127.0.0.1:5432/test_{random_str}'

        os.environ["TFA_CONFIG_NAME"] = "TEST"

        os.environ["TFA_DEVELOPMENT"] = "0"

    return AppConfig()


settings = get_config()
