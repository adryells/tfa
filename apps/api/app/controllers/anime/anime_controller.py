from app.controllers import BaseController
from app.controllers.anime.validator import UpdateAnimeData
from app.data.data import users_source
from app.data.media_type import anime_picture
from app.data.size_type import medium, large
from app.database.models.anime.basic import Anime
from app.database.queries.anime.anime_queries import AnimeQueries
from app.database.queries.media_item.media_item_queries import MediaItemQueries
from app.database.queries.request_change.request_change_queries import RequestChangeQueries
from app.database.queries.source_data.source_data_queries import SourceDataQueries


class AnimeController(BaseController):
    def validate_filters(self, page: int = None, per_page: int = None):
        if (page is not None and per_page is not None) and (per_page < 1 or page < 1):
            raise Exception("Invalid pagination.")

    def get_animes(self, sort_by: str = None, search: str = None, per_page: int = None, page: int = None) -> list[Anime]:
        self.validate_filters(per_page=per_page, page=page)

        animes = AnimeQueries(self.session).get_animes(sort_by=sort_by, search=search, per_page=per_page, page=page)

        return animes

    def get_anime_by_id(self, anime_id: int) -> Anime:
        anime = AnimeQueries(self.session).get_anime_by_id(anime_id=anime_id)

        if not anime:
            raise Exception("Anime not found.")

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

    def update_anime(self, data: UpdateAnimeData) -> Anime:
        anime = self.get_anime_by_id(data.anime_id)

        change_data = {
            "name": data.name,
            "average_ep_duration": data.average_ep_duration,
            "num_episodes": data.num_episodes,
            "synopsis": data.synopsis,
            "medium_image_id": data.medium_image_id,
            "large_image_id": data.large_image_id,
            "active": data.active,
            "source_data_id": data.source_data_id
        }

        if data.request_change_id:
            request_change = RequestChangeQueries(self.session).get_request_change_by_id(data.request_change_id)

            if not request_change:
                raise Exception("Request change not found.")

            for key, _ in change_data.items():
                value = request_change.change_data.get(key)

                if value:
                    change_data[key] = value

        handler = {
            "name": lambda: self.update_anime_name(anime, name=change_data["name"]),
            "average_ep_duration": lambda: self.update_attribute_object(anime, "average_ep_duration", change_data["average_ep_duration"]),
            "num_episodes": lambda: self.update_attribute_object(anime, "num_episodes", change_data["num_episodes"]),
            "synopsis": lambda: self.update_attribute_object(anime, "synopsis", change_data["synopsis"]),
            "medium_image_id": lambda: self.update_anime_media(
                size_type_name=medium.name,
                media_id=change_data["medium_image_id"],
                media_type_name=anime_picture.name,
                anime=anime
            ),
            "large_image_id": lambda: self.update_anime_media(
                size_type_name=large.name,
                media_id=change_data["large_image_id"],
                media_type_name=anime_picture.name,
                anime=anime
            ),
            "active": lambda: self.update_attribute_object(anime, "active", change_data["active"]),
            "source_data_id": lambda: self.update_anime_source_data(anime, change_data["source_data_id"])
        }

        for key, value in data.__dict__.items():
            if key in handler and value is not None:
                handler[key]()

        self.session.commit()

        return anime

    def update_anime_name(self, anime: Anime, name: str):
        if AnimeQueries(self.session).check_anime_exists_with_name(name):
            anime.name_conflicts = True

        anime.name = name

    def update_anime_media(self, anime: Anime, media_id: int, size_type_name: str, media_type_name: str):
        new_media = MediaItemQueries(self.session).get_media_item_by_id(media_id)

        if not new_media:
            raise Exception("Media Item not found.")

        if new_media.media_type.name != media_type_name:
            raise Exception("Wrong media type.")

        if new_media.size_type.name != size_type_name:
            raise Exception("Wrong size type.")

        for media in anime.related_media:
            if media.size_type.name == size_type_name and media.media_type.name == media_type_name:
                anime.related_media.remove(media)

        anime.related_media.append(new_media)

    def update_anime_source_data(self, anime: Anime, source_data_id: int):
        source_data = SourceDataQueries(self.session).get_source_data_by_id(source_data_id)

        if not source_data:
            raise Exception("Source data not found.")

        anime.source_data = source_data
