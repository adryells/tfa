from tests import BaseTest


class TestUpdateRequestChange(BaseTest):
    query = """
        mutation upreqchange($request_change_id: Int!, $accepted: Boolean!) {
          UpdateRequestChange(inputUpdateRequestChange: {
            requestChangeId: $request_change_id,
            accepted: $accepted
          }) {
            requestChange {
              accepted
              active
            }
          }
        }
    """

    def test_update_non_existent_request_change(self, client, admin_auth_token):
        self.assert_response_error(
            client=client,
            query=self.query,
            token=admin_auth_token.token,
            error_message="Request change not found.",
            variables={"request_change_id": 1000, "accepted": True}
        )

    def test_update_request_change_success(self, client, admin_auth_token, request_change):
        response = self.request_api(
            client=client,
            variables={"request_change_id": 1, "accepted": True},
            token=admin_auth_token.token,
            query=self.query
        )

        assert response["data"]["UpdateRequestChange"]["requestChange"]

        request_change_response = response["data"]["UpdateRequestChange"]["requestChange"]

        assert request_change_response["active"] is False
        assert request_change_response["accepted"] is True
