from typing import Optional

from pydantic import BaseModel, validator


class CalculateTFAData(BaseModel):
    available_hours: float
    title: str
    average_minutes_per_ep: float
    num_episodes: int

    @validator("available_hours")
    def validate_if_available_hours_is_not_equals_to_0(cls, value: float):
        if value <= 0:
            raise Exception("Available hours must be have at least one minute.")

        return value

    @validator("title")
    def validate_title(cls, value: str):
        stripped_value = value.strip()

        if not stripped_value:
            raise Exception("Title can't be blank.")

        return stripped_value


class UpdateAnimeData(BaseModel):
    anime_id: int
    name: Optional[str]
    synopsis: Optional[str]
    num_episodes: Optional[int]
    average_ep_duration: Optional[int]
    source_data_id: Optional[int]
    active: Optional[bool]
    request_change_id: Optional[int]
    medium_image_id: Optional[int]
    large_image_id: Optional[int]
