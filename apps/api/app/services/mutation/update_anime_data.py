from graphene import Mutation, InputObjectType, Int, String, Boolean, Field

from app.controllers.anime.anime_controller import AnimeController
from app.services.auth import graphql_authorizator
from app.services.types.anime import gAnime
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class InputUpdateAnimeData(InputObjectType):
    anime_id = Int(required=True)
    name = String()
    synopsys = String()
    num_episodes = Int()
    average_ep_duration = Int()
    source_data_id = Int()
    active = Boolean()
    medium_image_id = Int()
    large_image_id = Int()
    request_change_id = Int()


class UpdateAnimeData(Mutation):
    class Arguments:
        input_update_anime_data = InputUpdateAnimeData()

    anime = Field(gAnime)

    @graphql_authorizator
    def mutate(self, info: TFAGraphQLResolveInfo, input_update_anime_data: InputUpdateAnimeData):
        data = InputUpdateAnimeData(**input_update_anime_data.__dict__)

        anime = AnimeController(info.context.session).update_anime(data=data)

        return UpdateAnimeData(anime=anime) # noqa
