from pydantic import BaseModel


class SizeTypeData(BaseModel):
    name: str


medium = SizeTypeData(
    name="Medium"
)

large = SizeTypeData(
    name="Large"
)

size_types = [
    medium,
    large
]
