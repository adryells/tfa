from typing import Optional

from app.database.models.media.media_type import MediaType
from app.database.models.user.basic import User
from app.database.queries import BaseQueries
from app.database.models.media.basic import MediaItem


class MediaItemQueries(BaseQueries):
    def get_media_item_by_id(self, media_item_id: int) -> Optional[MediaItem]:
        media_item = self.session.query(MediaItem).filter(MediaItem.id == media_item_id).one_or_none()

        return media_item

    def get_media_item_by_user_id_and_type_slug(self, user_id: int, slug: str) -> Optional[MediaItem]:
        media_item = self.session.query(MediaItem)\
            .join(User.related_media)\
            .filter(User.id == user_id, MediaType.slug == slug)\
            .first()

        return media_item
