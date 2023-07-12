import math
from typing import Any

from faker import Faker
from starlette.testclient import TestClient


class BaseTest:
    fake = Faker()

    def request_api(self, test_client: TestClient, query: str, variables: dict[str, Any] = None) -> dict[str, Any]:
        query = {
            "variables": variables,
            "query": query
        }

        response = test_client.post(
            url="/graphql",
            json=query,
            headers={"content_type": 'application/json'}
        )

        return response.json()

    def assert_pagination_and_get_items(
            self,
            data: dict,
            total_count: int,
            page: int = 1,
            per_page: int = 10
    ) -> list[dict[str, Any]]:

        assert data["items"]
        assert data["page"]
        assert data["perPage"]
        assert data["pages"]
        assert data["totalCount"]

        assert data["perPage"] == per_page
        assert data["page"] == page

        assert data["totalCount"] == total_count
        assert data["pages"] == math.ceil(data["totalCount"] / data["perPage"])

        return data["items"]

    def assert_response_error(
            self,
            client: TestClient,
            query: str,
            variables: dict[str, Any],
            error_message: str
    ):
        response = self.request_api(
            test_client=client,
            variables=variables,
            query=query
        )

        assert response.get('errors')
        assert response['errors'][0]['message'] == error_message

    def assert_sorting_response(
            self,
            order_by_condition: str,
            reverse_list_condition: str,
            sorting_parameter: str,
            response_list: list[dict[str, Any]]
    ):
        reverse = True if order_by_condition == reverse_list_condition else False

        if isinstance(response_list[0][sorting_parameter], str):
            sorting_term = lambda item: item[sorting_parameter].lower().replace(" ", "")
        else:
            sorting_term = lambda item: item[sorting_parameter]

        manually_ordered_list = sorted(
            response_list,
            key=sorting_term,
            reverse=reverse
        )

        assert manually_ordered_list == response_list
