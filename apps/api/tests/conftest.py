import pytest
from faker import Faker
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from starlette.testclient import TestClient

from app.config import AppConfig, settings
from app.data import load_prod_data
from app.data.data import imagination_source
from app.database.base_class import DbBaseModel
from app.database.session import main_session, SessionLocal
from app.database.utils import init_db
from app.models.anime.basic import Anime
from app.queries.source_data.source_data_queries import SourceDataQueries
from app.services.router import graphql_app
from main import app
from tests.utils import DatabaseParameters

faker = Faker()


@pytest.fixture(scope="function", autouse=True)
def test_settings() -> AppConfig:
    return settings


@pytest.fixture(scope='function')
def db_engine(test_settings):
    database_parameters = DatabaseParameters.from_db_url(test_settings.DATABASE_URL)
    engine = create_engine(test_settings.DATABASE_URL)

    if not database_exists(engine.url):
        logger.info(f'Creating Database "{database_parameters.db_name}" for running tests...')
        create_database(engine.url)

    db_session = SessionLocal()

    init_db(db_session)
    load_prod_data(db_session, real_anime=False)

    yield engine

    logger.info(f'Dropping Database: "{database_parameters.db_name}"...')
    drop_database(test_settings.DATABASE_URL)


@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    connection.begin()

    database = scoped_session(sessionmaker(bind=connection, autoflush=False, autocommit=False))()

    yield database

    database.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[main_session] = lambda: db_session
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def session_middleware(db_session):

    def _session_middleware(next, root, info, **kwargs):
        info.context.session = db_session
        return next(root, info, **kwargs)

    graphql_app.middleware = [_session_middleware]


@pytest.fixture
def anime(db_session):
    source_data = SourceDataQueries(db_session).get_source_data_by_name(imagination_source.name)

    new_anime = Anime(
        name=faker.pystr(),
        num_episodes=faker.pyint(),
        average_ep_duration=faker.pyint(),
        source_data=source_data
    )

    db_session.add(new_anime)
    db_session.commit()

    return new_anime
