from typing import Optional

from pydantic import BaseModel


class RequestAnimeChangeData(BaseModel):
    anime_id: int
    reason: str
    additional_info: Optional[str]
    name: Optional[str]
    image_url: Optional[str]
    synopsis: Optional[str]
    num_episodes: Optional[int]
    average_ep_duration: Optional[int]
