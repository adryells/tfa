from app.database.models.media.media_type import MediaType
from app.database.models.user.basic import User
from app.database.queries import BaseQueries
from app.database.models.media.basic import MediaItem


class MediaItemQueries(BaseQueries):
    def get_media_item_by_id(self, media_item_id: int) -> MediaItem | None:
        media_item = self.session.query(MediaItem).filter(MediaItem.id == media_item_id).one_or_none()

        return media_item

    def get_media_item_by_user_id_and_type_name(self, user_id: int, name: str) -> MediaItem | None:
        media_item = self.session.query(MediaItem)\
            .join(User.related_media)\
            .filter(User.id == user_id, MediaType.name == name)\
            .first()

        return media_item
