from pydantic import BaseModel


class SizeTypeData(BaseModel):
    name: str
    slug: str


medium = SizeTypeData(
    name="Medium",
    slug="medium"
)

large = SizeTypeData(
    name="Large",
    slug="large"
)

size_types = [
    medium,
    large
]
