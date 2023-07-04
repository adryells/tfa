from pydantic import BaseModel


class SourceData(BaseModel):
    name: str


users_source = SourceData(
    name="User Requests"
)

mal_source = SourceData(
    name="My Anime List"
)

imagination_source = SourceData(
    name="My imagination"
)

sources = [users_source, mal_source, imagination_source]
