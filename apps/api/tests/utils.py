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


def create_user(session: Session, role_name: str) -> User:
    role = RoleQueries(session).get_role_by_name(role_name)

    new_user = User(
        role=role,
        username=fake.pystr(),
        email=fake.email()
    ).set_password("12345678")

    session.add(new_user)
    session.commit()

    return new_user
