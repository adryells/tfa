from graphene import Mutation, InputObjectType, String, Boolean, Field

from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class InputLoginData(InputObjectType):
    email = String(required=True)
    password = String(required=True)


class Login(Mutation):
    class Arguments:
        input_login_data = InputLoginData()

    auth_token = Field(gAuthToken)

    # busca usuario, ve se senha bate e gera token (desativa os existentes, cria o auth_token, gera e usa)
    def mutate(self, info: TFAGraphQLResolveInfo, input_login_data: InputLoginData):
        token = AuthTokenController(info.context.session).login(
            password=input_login_data.password,
            email=input_login_data.email,
            ip_address=info.context.request.client.host
        )

        return Login(auth_token=token)


class Logout(Mutation):
    success = Boolean()

    def mutate(self, info: TFAGraphQLResolveInfo):
        AuthTokenController(info.context.session).deactivate_auth_tokens(user_id=info.context.user.id)

        return Logout(success=True)
