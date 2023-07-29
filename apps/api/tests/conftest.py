import pytest
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from starlette.testclient import TestClient

from app.config import AppConfig, settings
from app.data import load_prod_data
from app.data.media_type import profile_picture
from app.data.role import common, admin
from app.database.models.anime.basic import Anime
from app.database.models.anime.request_change import RequestChange
from app.database.models.media.basic import MediaItem
from app.database.models.token.auth_token import AuthToken
from app.database.models.user.basic import User
from app.database.session import main_session, SessionLocal
from app.database.utils import init_db
from app.services.router import graphql_app
from main import app
from tests.utils import create_anime, create_request_change, create_user, create_media_item, create_auth_token

faker = Faker()


@pytest.fixture(scope="function", autouse=True)
def test_settings() -> AppConfig:
    return settings


@pytest.fixture(scope='function')
def db_engine(test_settings):
    engine = create_engine(test_settings.DATABASE_URL)

    if not database_exists(engine.url):
        create_database(engine.url)

    db_session = SessionLocal()

    init_db(db_session)
    load_prod_data(db_session)

    yield engine

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
def anime(db_session) -> Anime:
    new_anime = create_anime(db_session)

    return new_anime


@pytest.fixture
def animes(db_session) -> list[Anime]:
    anime_list = [create_anime(db_session) for _ in range(4)]

    return anime_list


@pytest.fixture
def request_change(db_session, anime) -> RequestChange:
    new_request_change = create_request_change(session=db_session, anime=anime)

    return new_request_change


@pytest.fixture
def request_changes(db_session, anime) -> list[RequestChange]:
    new_request_change = [create_request_change(session=db_session, anime=anime) for _ in range(4)]

    return new_request_change


@pytest.fixture
def common_user(db_session) -> User:
    user = create_user(db_session, role_name=common.name)

    return user


@pytest.fixture
def common_user_auth_token(db_session, common_user) -> AuthToken:
    auth_token = create_auth_token(db_session, user=common_user)

    return auth_token


@pytest.fixture
def admin_user(db_session) -> User:
    user = create_user(db_session, role_name=admin.name)

    return user


@pytest.fixture
def admin_auth_token(db_session, admin_user) -> AuthToken:
    auth_token = create_auth_token(db_session, user=admin_user)

    return auth_token


@pytest.fixture
def multiple_users(db_session) -> list[User]:
    user = [create_user(db_session, role_name=common.name) for _ in range(5)]

    return user


@pytest.fixture
def profile_picture_media(db_session, common_user) -> MediaItem:
    media = create_media_item(db_session, media_type_slug=profile_picture.name, creator=common_user)

    return media


@pytest.fixture
def anime_picture_media(db_session, common_user) -> MediaItem:
    media = create_media_item(db_session, creator=common_user)

    return media
