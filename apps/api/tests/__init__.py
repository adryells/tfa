import math
from typing import Any, Type

from faker import Faker
from graphene import ObjectType, NonNull
from starlette.testclient import TestClient

from app.database.base_class import DbBaseModel
from app.utils.string_utils import to_lower_camel_case


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

    def generate_query_with_fields(
            self,
            graphql_object: Type[ObjectType],
            model: Type[DbBaseModel],
            query_name: str,
            field_name: str,
            except_fields: list[str] = None,
            pagination_fields: bool = False
    ):
        graphql_object_name = graphql_object._meta.name
        field_args = graphql_object.__dict__[field_name].args.items()
        field_args = [
            {
                "name": arg[0],
                "type": arg[1].type._meta.name if type(arg[1].type) != NonNull else arg[1].type.of_type._meta.name,
                "required": type(arg[1].type) == NonNull
            }
            for arg in field_args
        ]

        variables = ', '.join(
            f"${to_lower_camel_case(arg['name'])}: {arg['type']}{'!' if arg['required'] else ''}"
            for arg in field_args
        )

        arguments = ', '.join(
            f"{to_lower_camel_case(arg['name'])}: ${to_lower_camel_case(arg['name'])}"
            for arg in field_args
        )

        chield_fields = "\n".join(
            to_lower_camel_case(attribute.key) for attribute in model.__table__.columns
            if attribute.key not in except_fields
        )

        chield_fields = f"""
            totalCount
            page
            perPage
            pages
            items{{
                {chield_fields}
            }}
        """ if pagination_fields else f"{chield_fields}"

        query = f"""
            query {query_name}({variables}){{
                  {graphql_object_name}{{
                    {field_name}({arguments}){{
                      {chield_fields}
                    }}
                }}
            }}
        """

        return query

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
