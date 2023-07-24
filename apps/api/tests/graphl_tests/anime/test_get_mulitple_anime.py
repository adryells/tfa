import pytest

from app.database.queries.anime.anime_queries import AnimeQueries
from tests import BaseTest


class TestMultipleAnime(BaseTest):
    query = """
        query getAnimes ($sortBy: AnimeSortByEnum, $search: String, $page: Int, $perpage: Int){
          Animes {
            animes(sortBy: $sortBy, search: $search, page: $page, perPage: $perpage) {
              totalCount
              page
              pages
              perPage
              items {
                id
                name
                numEpisodes
                averageEpDuration
                totalHours
                totalDays
              }
            }
          }
        }
    """

    all_sort_by_options = [
        ("TIME_TO_WATCH_ASC", "totalHours"),
        ("TIME_TO_WATCH_DESC", "totalHours"),
        ("NUM_EPISODES_ASC", "numEpisodes"),
        ("NUM_EPISODES_DESC", "numEpisodes"),
        ("TITLE_ASC", "name"),
        ("TITLE_DESC", "name"),
        ("AVERAGE_EP_DURATION_ASC", "averageEpDuration"),
        ("AVERAGE_EP_DURATION_DESC", "averageEpDuration")
    ]

    @pytest.fixture
    def variables(self, sort_by: str = None, search: str = None, page: int = 1, per_page: int = 10):
        return {
            "sortBy": sort_by,
            "search": search,
            "page": page,
            "perpage": per_page
        }

    @pytest.mark.parametrize("sort_by", all_sort_by_options)
    def test_get_anime_with_all_filters(self, client, db_session, sort_by, animes, variables):
        sorting_option, sorting_parameter = sort_by

        variables["sortBy"] = sorting_option
        variables["search"] = animes[0].name[0]

        response = self.request_api(
            test_client=client,
            variables=variables,
            query=self.query
        )

        assert not response.get("errors")

        assert response["data"]["Animes"]["animes"]

        animes_response = response["data"]["Animes"]["animes"]

        total_count = AnimeQueries(db_session).get_animes_count(variables["search"])

        items = self.assert_pagination_and_get_items(
            data=animes_response,
            per_page=variables["perpage"],
            page=variables["page"],
            total_count=total_count
        )

        for item in items:
            assert variables["search"].lower() in item["name"].lower()

        self.assert_sorting_response(
            order_by_condition=sorting_option,
            reverse_list_condition=sorting_option if "_DESC" in sorting_option else sorting_parameter + "_DESC",
            sorting_parameter=sorting_parameter,
            response_list=items
        )

    @pytest.mark.parametrize("page, per_page", [(0, 1), (1, 0)])
    def test_get_animes_with_invalid_pagination(self, client, page, per_page):
        self.assert_response_error(
            client=client,
            query=self.query,
            variables={"page": page, "perpage": per_page},
            error_message="Invalid pagination."
        )
