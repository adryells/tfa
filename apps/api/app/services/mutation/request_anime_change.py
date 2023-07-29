from graphene import Mutation, Boolean, InputObjectType, Int, String

from app.controllers.request_change.request_change_controller import RequestChangeController
from app.controllers.request_change.validator import RequestAnimeChangeData
from app.services.utils.custom_graphql_info import TFAGraphQLResolveInfo


class InputRequestAnimeChange(InputObjectType):
    anime_id = Int(required=True)
    reason = String(required=True)
    additional_info = String()
    name = String()
    image_url = String()
    synopsys = String()
    num_episodes = Int()
    average_ep_duration = Int()


class RequestAnimeChange(Mutation):
    class Arguments:
        input_request_anime_change = InputRequestAnimeChange()

    success = Boolean()

    def mutate(self, info: TFAGraphQLResolveInfo, input_request_anime_change: InputRequestAnimeChange): # noqa
        data = RequestAnimeChangeData(**input_request_anime_change.__dict__)

        RequestChangeController(info.context.session).request_anime_change(data=data)

        return RequestAnimeChange(success=True) # noqa
