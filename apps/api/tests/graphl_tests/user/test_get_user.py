from app.database.models.user.basic import User
from app.services.queries.user import User as GoUser
from tests import BaseTest
from tests.utils import format_date_graphql


class TestGetUserById(BaseTest):
    def request_query(self):
        return self.generate_query_with_fields(
            graphql_object=GoUser,
            query_name="getUserById",
            field_name="user",
            model=User,
            except_fields=["password", "password_salt"]
        )

    def test_get_user_by_id_success(self, client, common_user):
        response = self.request_api(
            client=client,
            variables={"userId": common_user.id},
            query=self.request_query()
        )

        assert not response.get("errors")

        assert response["data"]["User"]["user"]

        response_user = response["data"]["User"]["user"]

        assert response_user["id"] == common_user.id
        assert response_user["active"] == common_user.active
        assert response_user["username"] == common_user.username
        assert response_user["email"] == common_user.email
        assert response_user["roleId"] == common_user.role_id
        assert response_user["createdAt"] == format_date_graphql(common_user.created_at)
        assert response_user["updatedAt"] == common_user.updated_at

    def test_get_non_existent_user(self, client):
        self.assert_response_error(
            client=client,
            query=self.request_query(),
            error_message="User not found.",
            variables={"userId": 10}
        )
