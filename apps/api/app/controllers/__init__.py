from typing import Any

from sqlalchemy.orm import Session


class BaseController:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def update_attribute_object(obj: Any, attr: str, value: Any):
        if getattr(obj, attr) != value:
            setattr(obj, attr, value)
