from graphene import ObjectType, String, Argument, Int, Float, Mutation, InputObjectType, Field

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

    def mutate(self, _: TFAGraphQLResolveInfo, input_data: InputCalculateUnregisteredAnime):
        total_hours = (input_data.num_episodes * input_data.average_minutes_per_ep) / 60
        total_days = round(total_hours / 24, 2)

        if input_data.available_hours:
            days_predicted = round(total_hours / input_data.available_hours, 2)

        else:
            days_predicted = round(total_hours / 2, 2)

        result = CalculateUnregisteredAnime(
            TWAResult(days_predicted=days_predicted, total_days=total_days, total_hours=total_hours)
        )

        return result
