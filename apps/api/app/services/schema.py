from graphene import ObjectType, Schema

from app.services.mutation.auth_token import Login
from app.services.mutation.request_anime_change import RequestAnimeChange
from app.services.mutation.update_anime_data import UpdateAnime
from app.services.mutation.update_request_change import UpdateRequestChange
from app.services.mutation.user import CreateUser, UpdateUser, Signup, DeleteUser
from app.services.queries.anime import Animes
from app.services.mutation.calculate_tfa import CalculateTFA
from app.services.queries.request_change import RequestChange
from app.services.queries.user import User
from app.services.utils.graphql_mounter import mount_object


class Query(
    ObjectType,
    mount_object(Animes),
    mount_object(RequestChange),
    mount_object(User)
):
    pass


class Mutation(
    ObjectType,
    mount_object(CalculateTFA),
    mount_object(Login),
    mount_object(Signup),
    mount_object(CreateUser),
    mount_object(UpdateUser),
    mount_object(DeleteUser),
    mount_object(UpdateRequestChange),
    mount_object(RequestAnimeChange),
    mount_object(UpdateAnime)
):
    pass


graphql_schema = Schema(query=Query, mutation=Mutation)
