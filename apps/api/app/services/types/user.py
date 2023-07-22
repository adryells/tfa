from graphene import ObjectType, List

from app.models.user.basic import User
from app.services.types.generic import IdAsInt, PaginationData


class gUser(IdAsInt):
    class Meta:
        model = User


class Users(ObjectType, PaginationData):
    items = List(gUser)
