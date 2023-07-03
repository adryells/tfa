from graphene import ObjectType, Field, Int, Argument, String

from app.controllers.anime.anime_controller import AnimeController
from app.services.types.anime import gAnime, gAnimes
from app.services.types.enums import AnimeSortByEnum
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class Animes(ObjectType):
    anime = Field(gAnime, anime_id=Int(required=True))

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

        animes = anime_controller.get_animes(sort_by=sort_by, search=search)
        count = anime_controller.get_animes_count(search=search)

        return gAnimes(
            items=animes,
            total_count=count,
            page=page,
            per_page=per_page
        )
