import re

from faker import Faker
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.data.data import imagination_source
from app.database.models.anime.basic import Anime
from app.database.models.anime.request_change import RequestChange
from app.database.models.user.basic import User
from app.database.queries.role.role_queries import RoleQueries
from app.database.queries.source_data.source_data_queries import SourceDataQueries

fake = Faker()


class DatabaseParameters(BaseModel):
    schema_name: str = "postgresql"
    user: str
    password: str
    host: str
    port: int
    db_name: str

    @classmethod
    def from_db_url(cls, database_url: str) -> 'DatabaseParameters':
        schema, _, user, password, host, port, db_name = re.search(
            r"(.*?)\+(.*?)\:\/\/(.*?)\:(.*?)\@(.*)\:(.*)\/(.*)", database_url
        ).groups()

        return cls(
            schema_name=schema,
            user=user,
            password=password,
            host=host,
            port=port,
            db_name=db_name
        )


def format_date_graphql(string_date: str):
    return "T".join(str(string_date).split(" "))


def create_anime(session: Session):
    source_data = SourceDataQueries(session).get_source_data_by_name(imagination_source.name)

    new_anime = Anime(
        name=fake.name().lower(),
        num_episodes=fake.pyint(),
        average_ep_duration=fake.pyint(),
        source_data=source_data
    )

    session.add(new_anime)
    session.commit()

    return new_anime


def create_request_change(session: Session, anime: Anime):
    anime = anime or create_anime(session)

    new_request_change = RequestChange(
        anime=anime,
        change_data={
            "name": fake.pystr(),
            "average_ep_duration": fake.pyint(min_value=1, max_value=200),
            "num_episodes": fake.pyint(min_value=1, max_value=200),
            "synopsys": fake.text(),
            "image_url": fake.image_url()
        },
        reason=fake.pystr(),
        additional_info=fake.pystr()
    )

    session.add(new_request_change)
    session.commit()

    return new_request_change


def create_user(session: Session, name: str) -> User:
    role = RoleQueries(session).get_role_by_name(name)

    new_user = User(
        role=role,
        username=fake.pystr(),
        email=fake.email()
    ).set_password("12345678")

    session.add(new_user)
    session.commit()

    return new_user
