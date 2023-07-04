from graphene import ObjectType, String, Int, Float, Mutation, InputObjectType, Field

from app.controllers.anime.anime_controller import AnimeController
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class InputCalculateUnregisteredAnime(InputObjectType):
    num_episodes = Int(required=True)
    average_minutes_per_ep = Int(required=True)
    title = String(required=True)
    available_hours = Int(required=True)


class TWAResult(ObjectType):
    days_predicted = Float()
    total_days = Float()
    total_hours = Float()


class CalculateUnregisteredAnime(Mutation):
    class Arguments:
        input_data = InputCalculateUnregisteredAnime()

    result = Field(TWAResult)

    def mutate(self, info: TFAGraphQLResolveInfo, input_data: InputCalculateUnregisteredAnime):
        tfa_result = AnimeController(info.context.session).register_and_get_tfa_result(
            num_episodes=input_data.num_episodes,
            average_minutes_per_ep=input_data.average_minutes_per_ep,
            title=input_data.title,
            available_hours=input_data.available_hours
        )

        result = CalculateUnregisteredAnime(
            TWAResult(**tfa_result)
        )

        return result
