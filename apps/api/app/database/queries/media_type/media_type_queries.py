from app.database.queries import BaseQueries
from app.database.models.media.media_type import MediaType


class MediaTypeQueries(BaseQueries):
    def check_if_media_type_exists_by_name(self, name: str) -> bool:
        exists = self.session.query(
            self.session.query(MediaType.id).filter(MediaType.name == name).exists()
        ).scalar()

        return exists

    def get_media_type_by_name(self, name: str) -> MediaType | None:
        media_type = self.session.query(MediaType).filter(MediaType.name == name).one_or_none()

        return media_type
