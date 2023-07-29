from app.controllers import BaseController
from app.controllers.request_change.validator import RequestAnimeChangeData
from app.database.models.anime.request_change import RequestChange
from app.database.queries.anime.anime_queries import AnimeQueries
from app.database.queries.request_change.request_change_queries import RequestChangeQueries


class RequestChangeController(BaseController):
    def request_anime_change(self, data: RequestAnimeChangeData):
        anime = AnimeQueries(self.session).get_anime_by_id(data.anime_id)

        if not anime:
            raise Exception("Anime not found.")

        change_data = {
            "name": data.name,
            "average_ep_duration": data.average_ep_duration,
            "num_episodes": data.num_episodes,
            "synopsys": data.synopsys,
            "image_url": data.image_url
        }

        new_request_change = RequestChange(
            reason=data.reason,
            anime=anime,
            additional_info=data.additional_info,
            change_data=change_data
        )

        self.session.add(new_request_change)
        self.session.commit()

    def get_request_change_by_id(self, request_change_id: int) -> RequestChange:
        request_change = RequestChangeQueries(self.session).get_request_change_by_id(request_change_id)

        if not request_change:
            raise Exception("Request change not found.")

        return request_change

    def get_request_changes(self, anime_id: int = None, page: int = None, per_page: int = None):
        self.validate_filters(page=page, per_page=per_page, anime_id=anime_id)

        request_changes = RequestChangeQueries(self.session).get_request_changes(
            page=page,
            per_page=per_page,
            anime_id=anime_id
        )

        return request_changes

    def validate_filters(self, page: int = None, per_page: int = None, anime_id: int = None):
        if (page is not None and per_page is not None) and (per_page < 1 or page < 1):
            raise Exception("Invalid pagination.")

        if anime_id:
            existing_anime = AnimeQueries(self.session).check_anime_exists_with_id(anime_id=anime_id)

            if not existing_anime:
                raise Exception("Invalid anime id.")

    def get_request_changes_count(self, anime_id: int = None):
        self.validate_filters(anime_id=anime_id)

        count = RequestChangeQueries(self.session).get_request_changes_count(anime_id=anime_id)

        return count

    def update_request_change(self, request_change_id: int, accepted: bool) -> RequestChange:
        request_change = self.get_request_change_by_id(request_change_id)

        request_change.accepted = accepted
        request_change.active = False

        return request_change
