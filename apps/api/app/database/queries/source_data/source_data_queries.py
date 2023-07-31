from typing import Optional

from app.database.queries import BaseQueries
from app.database.models.data.basic import SourceData


class SourceDataQueries(BaseQueries):
    def check_source_data_exists_with_name(self, name: str) -> bool:
        exists = self.session.query(
            self.session.query(SourceData.id).filter(SourceData.name == name).exists()
        ).scalar()

        return exists

    def get_source_data_by_name(self, name: str) -> SourceData | None:
        source_data = self.session.query(SourceData).filter(SourceData.name == name).one_or_none()

        return source_data

    def get_source_data_by_id(self, source_data_id: int) -> SourceData | None:
        source_data = self.session.query(SourceData).filter(SourceData.id == source_data_id).one_or_none()

        return source_data
