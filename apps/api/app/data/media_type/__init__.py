from pydantic import BaseModel


class MediaTypeData(BaseModel):
    name: str
    slug: str


anime_picture = MediaTypeData(
    name="Anime Picture",
    slug="anime_picture"
)

profile_picture = MediaTypeData(
    name="Profile Picture",
    slug="profile_picture"
)

media_type_datas = [
    anime_picture,
    profile_picture
]
