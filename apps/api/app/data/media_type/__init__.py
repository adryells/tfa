from pydantic import BaseModel


class MediaTypeData(BaseModel):
    name: str


anime_picture = MediaTypeData(
    name="Anime Picture"
)

profile_picture = MediaTypeData(
    name="Profile Picture"
)

media_type_datas = [
    anime_picture,
    profile_picture
]
