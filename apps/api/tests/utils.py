import re

from faker import Faker
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.data.data import imagination_source
from app.models.anime.basic import Anime
from app.queries.source_data.source_data_queries import SourceDataQueries

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
