from graphene import ObjectType, List, Field

from app.data.media_type import profile_picture
from app.database.models.user.basic import User
from app.database.queries.media_item.media_item_queries import MediaItemQueries
from app.services.types.generic import IdAsInt, PaginationData
from app.services.types.media_item import gMediaItem
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class gUser(IdAsInt): # noqa
    class Meta:
        model = User

        exclude_fields = ["password", "password_salt"]

    profile_picture = Field(gMediaItem)

    def resolve_profile_picture(self, info: TFAGraphQLResolveInfo):
        media = MediaItemQueries(info.context.session).get_media_item_by_user_id_and_type_slug(
            user_id=self.id,
            slug=profile_picture.slug
        )

        return media


class Users(ObjectType, PaginationData):
    items = List(gUser)
