from graphene import Mutation, Field, InputObjectType, String, Boolean, Int

from app.controllers.user.user_controller import UserController
from app.data.permission import update_user, create_user, delete_user
from app.dto.user_dto import InputUpdateUserDataValidator, InputCreateUserDataValidator, InputSignupDataValidator
from app.services.auth import graphql_authorizator
from app.services.types.user import gUser
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class InputPassword(InputObjectType):
    current_password = String(required=True)
    new_password = String(required=True)


class InputCreateUserData(InputObjectType):
    username = String(required=True)
    email = String(required=True)
    role_id = Int(required=True)
    profile_picture_id = Int(required=True)
    active = Boolean(default_value=True)
    password = String(required=True)


class InputUpdateUserData(InputObjectType):
    user_id = Int(required=True)
    username = String()
    email = String()
    input_password = InputPassword()
    role_id = Int()
    profile_picture_id = Int()
    active = Boolean()


class InputSignupData(InputObjectType):
    username = String(required=True)
    email = String(required=True)
    password = String(required=True)


class CreateUser(Mutation):
    class Arguments:
        input_create_user_data = InputCreateUserData()

    user = Field(gUser)

    @graphql_authorizator(create_user.name)
    def mutate(self, info: TFAGraphQLResolveInfo, input_create_user_data: InputCreateUserData): # noqa
        validated_data = InputCreateUserDataValidator(**input_create_user_data.__dict__)

        user = UserController(info.context.session).create_user(data=validated_data)

        return CreateUser(user=user) # noqa


class UpdateUser(Mutation):
    class Arguments:
        input_update_user_data = InputUpdateUserData()

    user = Field(gUser)

    @graphql_authorizator(update_user.name)
    def mutate(self, info: TFAGraphQLResolveInfo, input_update_user_data: InputCreateUserData): # noqa
        validated_data = InputUpdateUserDataValidator(**input_update_user_data.__dict__)

        user = UserController(info.context.session).update_user(
            data=validated_data,
            updater_user_id=info.context.user.id
        )

        return UpdateUser(user=user) # noqa


class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)

    success = Boolean()

    @graphql_authorizator(delete_user.name)
    def mutate(self, info: TFAGraphQLResolveInfo, user_id: int): # noqa
        UserController(info.context.session).delete_user(user_id=user_id)

        return DeleteUser(success=True) # noqa


class Signup(Mutation):
    class Arguments:
        input_signup_data = InputSignupData()

    user = Field(gUser)

    def mutate(self, info: TFAGraphQLResolveInfo, input_signup_data: InputSignupData): # noqa
        validated_data = InputSignupDataValidator(**input_signup_data.__dict__)

        user = UserController(info.context.session).signup(data=validated_data)

        return Signup(user=user) # noqa
