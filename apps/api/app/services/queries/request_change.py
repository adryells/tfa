from graphene import ObjectType, Int, Field

from app.controllers.request_change.request_change_controller import RequestChangeController
from app.services.types.request_change import RequestChanges, gRequestChange
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class RequestChange(ObjectType):
    request_change = Field(gRequestChange, request_change_id=Int(required=True))

    request_changes = Field(
        RequestChanges,
        page=Int(default_value=1),
        per_page=Int(default_value=50),
        anime_id=Int()
    )

    def resolve_request_change(self, info: TFAGraphQLResolveInfo, request_change_id: int):
        request_change = RequestChangeController(info.context.session).get_request_change_by_id(request_change_id)

        return request_change

    def resolve_request_changes(
            self,
            info: TFAGraphQLResolveInfo,
            page: int = None,
            per_page: int = None,
            anime_id: int = None
    ):
        request_changes = RequestChangeController(info.context.session).get_request_changes(
            anime_id=anime_id,
            page=page,
            per_page=per_page
        )

        count = RequestChangeController(info.context.session).get_request_changes_count(anime_id=anime_id)

        return RequestChanges(
            items=request_changes,
            total_count=count,
            page=page,
            per_page=per_page
        )
