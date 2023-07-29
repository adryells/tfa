from graphene import Mutation, InputObjectType, Field, Int

from app.controllers.request_change.request_change_controller import RequestChangeController
from app.data.permission import update_request_change
from app.services.auth import graphql_authorizator
from app.services.types.request_change import gRequestChange
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class InputUpdateRequestChange(InputObjectType):
    request_change_id: int = Int(required=True)

    accepted: bool = Int(required=True)


class UpdateRequestChange(Mutation):
    class Arguments:
        input_update_request_change = InputUpdateRequestChange()

    request_change = Field(gRequestChange)

    @graphql_authorizator(update_request_change.name)
    def mutate(self, info: TFAGraphQLResolveInfo, input_update_request_change: InputUpdateRequestChange):
        request_change = RequestChangeController(info.context.session).update_request_change(
            request_change_id=input_update_request_change.request_change_id,
            accepted=input_update_request_change.accepted
        )

        return UpdateRequestChange(request_change=request_change) # noqa
