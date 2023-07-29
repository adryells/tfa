from app.database.queries.user.user_queries import UserQueries
from tests import BaseTest


class TestDeleteUser(BaseTest):
    query = """
        mutation deleteUser($userId: Int!){
          DeleteUser(userId: $userId){
            success
          }
        }
    """

    def test_request_without_token(self, client):
        self.assert_with_invalid_token(client=client, query=self.query, variables={"userId": 1})

    def test_request_with_invalid_structure_token(self, client):
        self.assert_with_invalid_token(
            client=client,
            query=self.query,
            token="hahaha 123",
            variables={"userId": 1}
        )

    def test_request_with_invalid_token(self, client):
        self.assert_with_invalid_token(
            client=client,
            query=self.query,
            token="TfaApiTok = isso ai",
            variables={"userId": 1},
            error_message="Token doesn't match any user."
        )

    def test_request_without_permission(self, client, common_user_auth_token):
        self.assert_with_invalid_token(
            client=client,
            query=self.query,
            token=common_user_auth_token.token,
            error_message="You don't have permission for this service.",
            variables={"userId": 1}
        )

    def test_delete_non_existent_user(self, client, admin_auth_token):
        self.assert_response_error(
            client=client,
            variables={"userId": 1000},
            error_message="User not found.",
            query=self.query,
            token=admin_auth_token.token
        )

    def test_delete_user_success(self, client, db_session, common_user, admin_auth_token):
        common_user_id = common_user.id

        response = self.request_api(
            client=client,
            query=self.query,
            variables={"userId": common_user_id},
            token=admin_auth_token.token
        )

        assert response["data"]["DeleteUser"]["success"]
        assert not UserQueries(db_session).get_user_by_id(common_user_id)
