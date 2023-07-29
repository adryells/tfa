from graphene import ObjectType, String, Int, Float, Mutation, InputObjectType, Field

from app.controllers.anime.anime_controller import AnimeController
from app.controllers.anime.validator import CalculateTFAData
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class InputCalculateTFA(InputObjectType):
    num_episodes = Int(required=True)
    average_minutes_per_ep = Float(required=True)
    title = String(required=True)
    available_hours = Float(required=True)


class TFAResult(ObjectType):
    days_predicted = Float()
    total_days = Float()
    total_hours = Float()


class CalculateTFA(Mutation):
    class Arguments:
        input_data = InputCalculateTFA()

    result = Field(TFAResult)

    def mutate(self, info: TFAGraphQLResolveInfo, input_data: InputCalculateTFA): # noqa
        validated_data = CalculateTFAData(**input_data.__dict__)

        tfa_result = AnimeController(info.context.session).register_and_get_tfa_result(
            num_episodes=validated_data.num_episodes,
            average_minutes_per_ep=validated_data.average_minutes_per_ep,
            title=validated_data.title,
            available_hours=validated_data.available_hours
        )

        result = CalculateTFA(TFAResult(**tfa_result)) # noqa

        return result
