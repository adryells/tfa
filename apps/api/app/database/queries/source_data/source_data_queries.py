from typing import Optional

from app.database.queries import BaseQueries
from app.database.models.data.basic import SourceData


class SourceDataQueries(BaseQueries):
    def check_source_data_exists_with_slug(self, slug: str) -> bool:
        exists = self.session.query(
            self.session.query(SourceData.id).filter(SourceData.slug == slug).exists()
        ).scalar()

        return exists

    def get_source_data_by_slug(self, slug: str) -> Optional[SourceData]:
        source_data = self.session.query(SourceData).filter(SourceData.slug == slug).one_or_none()

        return source_data

    def get_source_data_by_id(self, source_data_id: int) -> Optional[SourceData]:
        source_data = self.session.query(SourceData).filter(SourceData.id == source_data_id).one_or_none()

        return source_data
