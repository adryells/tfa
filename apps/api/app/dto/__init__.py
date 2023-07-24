from pydantic import BaseModel


class BaseValidator(BaseModel):
    @classmethod
    def validate_id(cls, value: int | str):
        return value < 1 if value else None
