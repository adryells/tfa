from typing import Union

from pydantic import BaseModel


class BaseValidator(BaseModel):
    @classmethod
    def validate_id(cls, value: Union[str, int]):
        return value < 1 if value else None
