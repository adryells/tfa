from graphene import ObjectType, List

from app.database.models.user.basic import User
from app.services.types.generic import IdAsInt, PaginationData


class gUser(IdAsInt):
    class Meta:
        model = User

        exclude_fields = ["password", "password_salt"]


class Users(ObjectType, PaginationData):
    items = List(gUser)
