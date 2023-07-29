from graphene import Mutation, InputObjectType, String, Field

from app.controllers.auth_token.auth_token_controller import AuthTokenController
from app.services.types.auth_token import gAuthToken
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class InputLoginData(InputObjectType):
    email = String(required=True)
    password = String(required=True)


class Login(Mutation):
    class Arguments:
        input_login_data = InputLoginData()

    auth_token = Field(gAuthToken)

    def mutate(self, info: TFAGraphQLResolveInfo, input_login_data: InputLoginData):  # noqa

        token = AuthTokenController(info.context.session).login(
            password=input_login_data.password, # noqa
            email=input_login_data.email, # noqa
            ip_address=info.context.request.client.host
        )

        return Login(auth_token=token) # noqa
