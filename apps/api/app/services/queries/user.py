from graphene import ObjectType, Field, Int, String

from app.controllers.user.user_controller import UserController
from app.services.types.user import gUser, Users
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class User(ObjectType):
    user = Field(gUser, user_id=Int(required=True))
    users = Field(
        Users,
        user_id=Int(required=True),
        search=String(),
        page=Int(default_value=1),
        per_page=Int(default_value=50)
    )

    def resolve_user(self, info: TFAGraphQLResolveInfo, user_id: int):
        user = UserController(info.context.session).get_user_by_id(user_id)

        return user

    def resolve_users(self, info: TFAGraphQLResolveInfo, search: str = None, page: int = 1, per_page: int = None):
        user_controller = UserController(info.context.session)

        users = user_controller.get_users(page=page, per_page=per_page, search=search)

        total_count = user_controller.get_users_count(search=search)

        return Users(
            total_count=total_count,
            items=users,
            page=page,
            per_page=per_page
        )
