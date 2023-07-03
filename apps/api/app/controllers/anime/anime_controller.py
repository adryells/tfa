from app.controllers import BaseController
from app.data.data import users_source
from app.models.anime.basic import Anime
from app.queries.anime.anime_queries import AnimeQueries
from app.queries.source_data.source_data_queries import SourceDataQueries


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

    def register_and_get_tfa_result(
            self,
            num_episodes: float,
            average_minutes_per_ep: float,
            title: str,
            available_hours: float = 2
    ):
        self.register_unchecked_anime(
            num_episodes=num_episodes,
            average_minutes_per_ep=average_minutes_per_ep,
            title=title
        )

        total_hours = (num_episodes * average_minutes_per_ep) / 60
        total_days = round(total_hours / 24, 2)

        days_predicted = round(total_hours / available_hours, 2)

        return {
            "days_predicted": days_predicted,
            "total_days": total_days,
            "total_hours": total_hours
        }

    def register_unchecked_anime(
            self,
            num_episodes: float,
            average_minutes_per_ep: float,
            title: str
    ) -> Anime:
        source_data = SourceDataQueries(self.session).get_source_data_by_name(name=users_source.name)

        name_conflicts = AnimeQueries(self.session).check_anime_exists_with_name(name=title)

        anime = Anime(
            num_episodes=num_episodes,
            average_ep_duration=average_minutes_per_ep,
            active=False,
            source_data=source_data,
            name=title,
            name_conflicts=name_conflicts
        )

        self.session.add(anime)
        self.session.commit()

        return anime
