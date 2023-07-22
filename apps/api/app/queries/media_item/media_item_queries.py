from app.database.queries import BaseQueries
from app.models.media.basic import MediaItem


class MediaItemQueries(BaseQueries):
    def get_media_item_by_id(self, media_item_id: int) -> MediaItem | None:
        media_item = self.session.query(MediaItem).filter(MediaItem.id == media_item_id).one_or_none()

        return media_item
