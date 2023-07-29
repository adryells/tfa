import pytest

from app.database.models.user.basic import User
from app.database.queries.user.user_queries import UserQueries
from app.services.queries.user import User as GoUser
from tests import BaseTest


class TestGetUsers(BaseTest):
    def request_query(self):
        return self.generate_query_with_fields(
            graphql_object=GoUser,
            query_name="getUsers",
            field_name="users",
            model=User,
            pagination_fields=True,
            except_fields=["password", "password_salt"]
        )

    @pytest.mark.parametrize("page, per_page", [(0, 1), (1, 0)])
    def test_get_users_with_invalid_pagination(self, client, page, per_page):
        self.assert_response_error(
            client=client,
            query=self.request_query(),
            variables={"page": page, "perPage": per_page},
            error_message="Invalid Pagination."
        )

    def test_get_users_with_filters_success(self, client, db_session, multiple_users):
        keyword = multiple_users[0].username[0]

        response = self.request_api(
            client=client,
            variables={"page": 1, "perPage": 5, "search": keyword},
            query=self.request_query()
        )

        assert response["data"]["User"]["users"]

        users_response = response["data"]["User"]["users"]

        total_count = UserQueries(db_session).get_users_count(search=keyword)

        items = self.assert_pagination_and_get_items(
            data=users_response,
            per_page=5,
            page=1,
            total_count=total_count
        )

        for item in items:
            assert keyword.lower() in item["username"].lower()
