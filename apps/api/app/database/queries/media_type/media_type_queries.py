from typing import Optional

from app.database.queries import BaseQueries
from app.database.models.media.media_type import MediaType


class MediaTypeQueries(BaseQueries):
    def check_if_media_type_exists_by_slug(self, slug: str) -> bool:
        exists = self.session.query(
            self.session.query(MediaType.id).filter(MediaType.slug == slug).exists()
        ).scalar()

        return exists

    def get_media_type_by_slug(self, slug: str) -> Optional[MediaType]:
        media_type = self.session.query(MediaType).filter(MediaType.slug == slug).one_or_none()

        return media_type
