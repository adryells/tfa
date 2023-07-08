from app.controllers import BaseController
from app.controllers.request_change.validator import RequestAnimeChangeData
from app.models.anime.request_change import RequestChange
from app.queries.anime.anime_queries import AnimeQueries


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
        pass
