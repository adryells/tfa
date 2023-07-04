from app.database.queries import BaseQueries
from app.models.media.size_type import SizeType


class SizeTypeQueries(BaseQueries):
    def check_size_type_exists_with_name(self, name: str) -> bool:
        exists = self.session.query(
            self.session.query(SizeType.id).filter(SizeType.name == name).exists()
        ).scalar()

        return exists

    def get_size_type_by_name(self, name: str) -> SizeType:
        size_type = self.session.query(SizeType).filter(SizeType.name == name).one_or_none()

        return size_type
