from app.database.queries import BaseQueries
from app.database.models.media.size_type import SizeType


class SizeTypeQueries(BaseQueries):
    def check_size_type_exists_by_slug(self, slug: str) -> bool:
        exists = self.session.query(
            self.session.query(SizeType.id).filter(SizeType.slug == slug).exists()
        ).scalar()

        return exists

    def get_size_type_by_slug(self, slug: str) -> SizeType:
        size_type = self.session.query(SizeType).filter(SizeType.slug == slug).one_or_none()

        return size_type
