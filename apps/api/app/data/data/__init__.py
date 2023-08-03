from pydantic import BaseModel


class SourceData(BaseModel):
    name: str
    slug: str


users_source = SourceData(
    name="User Requests",
    slug="user_requests"
)

mal_source = SourceData(
    name="My Anime List",
    slug="my_anime_list"
)

imagination_source = SourceData(
    name="My imagination",
    slug="my_imagination"
)

sources = [users_source, mal_source, imagination_source]
