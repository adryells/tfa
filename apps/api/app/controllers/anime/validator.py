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


class InputUpdateAnimeData(BaseModel):
    anime_id: int
    name: str | None
    synopsys: str | None
    num_episodes: int | None
    average_ep_duration: int | None
    source_data_id: int | None
    active: bool | None
    request_change_id: int | None
    medium_image_id: int | None
    large_image_id: int | None
