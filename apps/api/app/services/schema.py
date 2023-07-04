from graphene import ObjectType, Schema

from app.services.queries.anime import Animes
from app.services.mutation.calculate_tfa import CalculateTFA
from app.services.utils.graphql_mounter import mount_object


class Query(
    ObjectType,
    mount_object(Animes)
):
    pass


class Mutation(
    ObjectType,
    mount_object(CalculateTFA)
):
    pass


graphql_schema = Schema(query=Query, mutation=Mutation)
