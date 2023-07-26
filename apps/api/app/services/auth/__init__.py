from functools import wraps

from app.database.queries.permission.permission_queries import PermissionQueries
from app.database.queries.user.user_queries import UserQueries
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class GraphqlAuth:

    def __init__(self, permission_name: str = None):
        self.permission_name = permission_name

    def __call__(self, fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            graphql_info: TFAGraphQLResolveInfo = args.__getitem__(1)
            authorization_token = graphql_info.context.authorization

            if not authorization_token:
                raise Exception("Authorization token is required.")

            if not authorization_token.startswith("TfaApiTok = "):
                raise Exception("Invalid token structure.")

            token = authorization_token.split("= ")[-1]

            user = UserQueries(graphql_info.context.session).get_user_by_token(token)

            if not user:
                raise Exception("Token doesn't match any user.")

            graphql_info.context.user = user

            if not self.permission_name:
                return fn(*args, **kwargs)

            user_has_permission = PermissionQueries(graphql_info.context.session).get_role_has_permission(
                role_id=user.role_id,
                permission_name=self.permission_name
            )

            if not user_has_permission:
                raise Exception("You don't have permission for this service.")

            return fn(*args, **kwargs)

        return decorator


def graphql_authorizator(permission_name: str = None) -> GraphqlAuth:
    return GraphqlAuth(permission_name=permission_name)
