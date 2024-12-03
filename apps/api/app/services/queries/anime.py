from graphene import ObjectType, Field, Int, Argument, String

from app.controllers.anime.anime_controller import AnimeController
from app.services.types.anime import gAnime, gAnimes
from app.services.types.enums import AnimeSortByEnum
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo
from app.utils.redis_cache import RedisCacheController


class Animes(ObjectType):
    anime = Field(gAnime, anime_id=Argument(Int(required=True)))

    animes = Field(
        gAnimes,
        sort_by=Argument(AnimeSortByEnum),
        search=Argument(String),
        page=Argument(Int, default_value=1),
        per_page=Argument(Int, default_value=50)
    )

    def resolve_anime(self, info: TFAGraphQLResolveInfo, anime_id: int):
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
        redis_cache_controller = RedisCacheController()

        cache_key = f"anime:{sort_by}-{search}-{page}-{per_page}"

        anime_cached = redis_cache_controller.get_data(cache_key)
        total_anime_cached = redis_cache_controller.get_data(f"anime_count:{sort_by}-{search}-{page}-{per_page}")

        if anime_cached and total_anime_cached:
            items = anime_cached
            total = total_anime_cached

        else:
            items = anime_controller.get_animes(sort_by=sort_by, search=search, per_page=per_page, page=page)
            total = anime_controller.get_animes_count(search=search)

            redis_cache_controller.set_data(cache_key, items)

        return gAnimes(
            items=items,
            total_count=total,
            page=page,
            per_page=per_page
        )
