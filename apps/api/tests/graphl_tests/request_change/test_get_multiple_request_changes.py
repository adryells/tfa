import pytest

from app.database.queries.request_change_queries import RequestChangeQueries
from tests import BaseTest


class TestGetMultipleRequestChange(BaseTest):
    query = """
        query requestChange ($page: Int, $perPage: Int, $animeId: Int){
          RequestChange{
            requestChanges(page: $page, perPage: $perPage, animeId: $animeId){
            page
            perPage
            totalCount
            pages
              items{
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
        }
    """

    @pytest.fixture
    def variables(self, page: int = 1, per_page: int = 10, anime_id: int = 1):
        return {
            "page": page,
            "perPage": per_page,
            "animeId": anime_id
        }

    def test_get_multiple_request_change(self, client, db_session, request_changes, variables):
        response = self.request_api(
            test_client=client,
            variables=variables,
            query=self.query
        )

        assert response["data"]["RequestChange"]["requestChanges"]

        request_changes_response = response["data"]["RequestChange"]["requestChanges"]

        total_count = RequestChangeQueries(db_session).get_request_changes_count(anime_id=1)

        items = self.assert_pagination_and_get_items(
            data=request_changes_response,
            per_page=variables["perPage"],
            page=variables["page"],
            total_count=total_count
        )

        for item in items:
            assert item["animeId"] == 1

    def test_get_multiple_request_changes_with_invalid_anime(self, client):
        self.assert_response_error(
            client=client,
            error_message="Invalid anime id.",
            variables={"animeId": 100},
            query=self.query
        )
