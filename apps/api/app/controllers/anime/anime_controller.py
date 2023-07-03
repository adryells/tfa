from app.controllers import BaseController
from app.models.anime.basic import Anime
from app.queries.anime.anime_queries import AnimeQueries


class AnimeController(BaseController):
    def get_animes(self, sort_by: str = None, search: str = None) -> list[Anime]:
        animes = AnimeQueries(self.session).get_animes(sort_by=sort_by, search=search)

        return animes

    def get_anime_by_id(self, anime_id: int) -> Anime:
        anime = AnimeQueries(self.session).get_anime_by_id(anime_id=anime_id)

        return anime

    def get_animes_count(self, search: str = None) -> int:
        count = AnimeQueries(self.session).get_animes_count(search=search)

        return count
