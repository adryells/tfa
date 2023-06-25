import math

from graphene import Field, Int
from graphene_sqlalchemy import SQLAlchemyObjectType # noqa


class PaginationData:
    total_count = Int()

    page = Field(Int, default_value=1)
    per_page = Field(Int, default_value=50)

    pages = Field(Int)

    def resolve_pages(self, _):
        return math.ceil(float(self.total_count) / self.per_page) # noqa


class IdAsInt(SQLAlchemyObjectType):
    class Meta:
        abstract = True

    id = Int()
