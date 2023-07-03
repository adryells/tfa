from graphene import ObjectType, Schema

from app.services.queries.anime import Animes
from app.services.mutation.twa import CalculateUnregisteredAnime
from app.services.utils.graphql_mounter import mount_object


class Query(
    ObjectType,
    mount_object(Animes)
):
    pass


class Mutation(
    ObjectType,
    mount_object(CalculateUnregisteredAnime)
):
    pass


graphql_schema = Schema(query=Query, mutation=Mutation)
