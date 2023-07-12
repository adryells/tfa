from pydantic import BaseModel


class RequestAnimeChangeData(BaseModel):
    anime_id: int
    reason: str
    additional_info: str | None
    name: str | None
    image_url: str | None
    synopsys: str | None
    num_episodes: int | None
    average_ep_duration: int | None
