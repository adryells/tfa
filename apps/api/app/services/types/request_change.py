from graphene import ObjectType, List

from app.models.anime.request_change import RequestChange
from app.services.types.generic import IdAsInt, PaginationData


class gRequestChange(IdAsInt):
    class Meta:
        model = RequestChange


class RequestChanges(ObjectType, PaginationData):
    items = List(gRequestChange)
