import json

from tests import BaseTest


class TestGetOneRequestChange(BaseTest):
    query = """
        query requestChange ($requestChangeId: Int!){
          RequestChange{
            requestChange(requestChangeId: $requestChangeId){
              createdAt
              id
              changeData
              reason
              additionalInfo
              active
              accepted
              animeId
            }
          }
        }
    """

    def test_get_one_request_change_success(self, client, request_change):
        response = self.request_api(
            client=client,
            variables={"requestChangeId": request_change.id},
            query=self.query
        )

        assert not response.get("errors")

        assert response["data"]["RequestChange"]["requestChange"]

        request_change_response = response["data"]["RequestChange"]["requestChange"]

        assert request_change_response["id"] == request_change.id
        assert request_change_response["reason"] == request_change.reason
        assert request_change_response["additionalInfo"] == request_change.additional_info
        assert request_change_response["active"] == request_change.active
        assert request_change_response["accepted"] == request_change.accepted
        assert request_change_response["changeData"]

        change_data_response = json.loads(request_change_response["changeData"])

        assert change_data_response["name"] == request_change.change_data["name"]
        assert change_data_response["average_ep_duration"] == request_change.change_data["average_ep_duration"]
        assert change_data_response["num_episodes"] == request_change.change_data["num_episodes"]
        assert change_data_response["synopsis"] == request_change.change_data["synopsis"]
        assert change_data_response["image_url"] == request_change.change_data["image_url"]

    def test_get_invalid_request_change(self, client):
        self.assert_response_error(
            client=client,
            query=self.query,
            variables={"requestChangeId": 100},
            error_message="Request change not found."
        )
