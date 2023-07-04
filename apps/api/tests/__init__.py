import math
from typing import Dict, Any, List, Type

from faker import Faker
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.database.base_class import DbBaseModel


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
            db_session: Session,
            query_name: str,
            client: TestClient,
            query: str,
            page: int = 1,
            per_page: int = 4,
            model_name: str = None
    ) -> List[Dict[str, Any]]:
        variables = {
            "page": page,
            "perpage": per_page
        }

        response = self.request_api(
            test_client=client,
            variables=variables,
            query=query
        )

        assert not response.get("errors")
        assert response["data"][query_name]["all"]

        response_all = response["data"][query_name]["all"]

        assert response_all["items"]
        assert response_all["page"]
        assert response_all["perpage"]
        assert response_all["pages"]
        assert response_all["totalCount"]

        assert variables["perpage"] == response_all["perpage"]
        assert response_all["page"] == variables["page"]

        model_name = model_name or query_name

        model = self.get_model_from_name(name=model_name)

        assert response_all["totalCount"] == db_session.query(model).count()
        assert response_all["pages"] == math.ceil(response_all["totalCount"] / response_all["perpage"])

        return response_all["items"]

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

    def get_model_from_name(self, name) -> Type[DbBaseModel]:
        model = [
            model_class for model_class in DbBaseModel.__subclasses__()
            if model_class.__name__ == name
        ][0]

        return model
