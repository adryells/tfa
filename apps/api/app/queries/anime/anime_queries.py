from sqlalchemy import asc, desc
from sqlalchemy.orm import Query

from app.database.queries import BaseQueries
from app.models.anime.basic import Anime


class AnimeQueries(BaseQueries):
    def get_anime_by_id(self, anime_id: int) -> Anime | None:
        anime = self.get_one_or_none_by_id(Anime, anime_id)

        return anime

    def get_animes(self, page: int = None, per_page: int = None, sort_by: str = None, search: str = None):
        query = self._get_animes_query(sort_by=sort_by, search=search)

        if page and per_page:
            query = self.get_query_with_pagination(query=query, page=page, per_page=per_page)

        return query.all()

    def get_animes_count(self, search: str = None) -> int:
        query = self._get_animes_query(search=search)

        return query.count()

    def _get_animes_query(self, sort_by: str = None, search: str = None) -> Query:
        query = self.session.query(Anime)

        if search:
            search = f"%{search}%"

            query = query.filter(Anime.name.ilike(search))

        if sort_by:
            order_handler = {
                "TIME_TO_WATCH_ASC": lambda: query.order_by(asc(Anime.total_hours)),
                "TIME_TO_WATCH_DESC": lambda: query.order_by(desc(Anime.total_hours)),
                "NUM_EPISODES_ASC": lambda: query.order_by(Anime.num_episodes.asc()),
                "NUM_EPISODES_DESC": lambda: query.order_by(Anime.num_episodes.desc()),
                "TITLE_ASC": lambda: query.order_by(Anime.name.asc()),
                "TITLE_DESC": lambda: query.order_by(Anime.name.desc()),
                "AVERAGE_EP_DURATION_ASC": lambda: query.order_by(Anime.average_ep_duration.asc()),
                "AVERAGE_EP_DURATION_DESC": lambda: query.order_by(Anime.average_ep_duration.desc())
            }

            query = order_handler[sort_by]()

        return query

    def check_anime_exists_with_name(self, name: str) -> bool:
        exists = self.session.query(
            self.session.query(Anime.id).filter(Anime.name == name).exists()
        ).scalar()

        return exists
