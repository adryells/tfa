from typing import Optional

from sqlalchemy.orm import Query

from app.database.queries import BaseQueries
from app.database.models.anime.request_change import RequestChange


class RequestChangeQueries(BaseQueries):
    def get_request_change_by_id(self, request_change_id: int) -> Optional[RequestChange]:
        request_change = self.get_one_or_none_by_id(RequestChange, request_change_id)

        return request_change

    def get_request_changes(self, page: int = None, per_page: int = None, anime_id: int = None):
        query = self._get_request_changes_query(anime_id=anime_id)

        if page and per_page:
            query = self.get_query_with_pagination(query, page, per_page)

        return query.all()

    def _get_request_changes_query(self, anime_id: int = None) -> Query:
        query = self.session.query(RequestChange)

        if anime_id:
            query = query.filter(RequestChange.anime_id == anime_id)

        return query

    def get_request_changes_count(self, anime_id: int) -> int:
        count = self._get_request_changes_query(anime_id=anime_id).count()

        return count
