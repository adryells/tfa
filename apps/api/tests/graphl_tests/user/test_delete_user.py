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

    def test_delete_non_existent_user(self, client):
        self.assert_response_error(
            client=client,
            variables={"userId": 1000},
            error_message="User not found.",
            query=self.query
        )

    def test_delete_user_success(self, client, db_session, common_user):
        common_user_id = common_user.id

        response = self.request_api(
            test_client=client,
            query=self.query,
            variables={"userId": common_user_id}
        )

        assert response["data"]["DeleteUser"]["success"]
        assert not UserQueries(db_session).get_user_by_id(common_user_id)
