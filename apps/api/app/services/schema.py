from graphene import ObjectType, Schema

from app.queries.teste import Teste
from app.services.utils.graphql_mounter import mount_object


class Query(
    ObjectType,
    mount_object(Teste)
):
    pass


class Mutation(ObjectType):
    pass


graphql_schema = Schema(query=Query)
