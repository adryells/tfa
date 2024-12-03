import json

from graphene import ObjectType, Field, Int, Argument, String

from app.controllers.anime.anime_controller import AnimeController
from app.database.models.anime.basic import Anime
from app.database.redis_client import redis_client
from app.services.types.anime import gAnime, gAnimes
from app.services.types.enums import AnimeSortByEnum
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class Animes(ObjectType):
    anime = Field(gAnime, anime_id=Argument(Int(required=True)))

    animes = Field(
        gAnimes,
        sort_by=Argument(AnimeSortByEnum),
        search=Argument(String),
        page=Argument(Int, default_value=1),
        per_page=Argument(Int, default_value=50)
    )

    async def resolve_anime(self, info: TFAGraphQLResolveInfo, anime_id: int):
        anime = AnimeController(info.context.session).get_anime_by_id(anime_id=anime_id)

        return anime

    def resolve_animes(
            self,
            info: TFAGraphQLResolveInfo,
            sort_by: str = None,
            search: str = None,
            page: int = None,
            per_page: int = None
    ):
        anime_controller = AnimeController(info.context.session)

        cache_key = f":{sort_by}-{search}-{page}-{per_page}"
        anime_key = f"anime{cache_key}"
        total_count_key = f"anime_count{cache_key}"

        anime_cached = redis_client.get(anime_key)
        total_anime_cached = redis_client.get(total_count_key)

        if anime_cached and total_anime_cached:
            items = json.loads(anime_cached)
            total = total_anime_cached

        else:
            animes = anime_controller.get_animes(sort_by=sort_by, search=search, per_page=per_page, page=page)
            total = anime_controller.get_animes_count(search=search)
            items = [anime.to_dict() for anime in animes]

            redis_client.set(anime_key, json.dumps(items), ex=120)
            redis_client.set(total_count_key, total, ex=120)

        response_animes = []
        for item in items:
            response_animes.append(
                Anime(
                    active=item.get("active"),
                    average_ep_duration=item.get("average_ep_duration"),
                    id=item.get("id"),
                    name=item.get("name"),
                    name_conflicts=item.get("name_conflicts"),
                    num_episodes=item.get("num_episodes"),
                    original_id=item.get("original_id"),
                    source_data_id=item.get("source_data_id"),
                    synopsis=item.get("synopsis")
                )
            )


        return gAnimes(
            items=response_animes,
            total_count=total,
            page=page,
            per_page=per_page
        )
