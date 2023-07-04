import re

from pydantic import BaseModel


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
