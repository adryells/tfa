from typing import Any

import pytest

from app.data.data import users_source
from app.models.anime.basic import Anime
from app.queries.source_data.source_data_queries import SourceDataQueries
from tests import BaseTest


class TestCalculateTFA(BaseTest):
    query = """
        mutation registerAnime (
          $numEpisodes: Int!,
          $averageMinutesPerEp: Float!,
          $title: String!,
          $availableHours: Float!
        ){
          CalculateTFA(inputData:{
            numEpisodes: $numEpisodes,
            averageMinutesPerEp: $averageMinutesPerEp,
            title: $title,
            availableHours: $availableHours
          }){
            result{
              daysPredicted
              totalDays
              totalHours
            }
          }
        }
    """

    @pytest.fixture
    def variables(self) -> dict[str, Any]:
        return {
            "availableHours": self.fake.pyfloat(min_value=1, max_value=3, right_digits=2),
            "numEpisodes": self.fake.pyint(min_value=1, max_value=256),
            "title": self.fake.name(),
            "averageMinutesPerEp": self.fake.pyfloat(min_value=10, max_value=60, right_digits=2)
        }

    def assert_request_worked(self, response, variables, db_session):
        assert not response.get("errors")

        assert response["data"]["CalculateTFA"]

        response_calculate_tfa = response["data"]["CalculateTFA"]["result"]

        total_hours = (variables["numEpisodes"] * variables["averageMinutesPerEp"]) / 60
        total_days = total_hours / 24

        days_predicted = round(total_hours / variables["availableHours"], 2)

        assert response_calculate_tfa["daysPredicted"] == days_predicted
        assert response_calculate_tfa["totalHours"] == total_hours
        assert response_calculate_tfa["totalDays"] == round(total_days, 2)

        new_anime: Anime = db_session.query(Anime).filter(Anime.name == variables["title"]).order_by(
            Anime.id.desc()).first()

        assert new_anime.num_episodes == variables["numEpisodes"]
        assert new_anime.average_ep_duration == variables["averageMinutesPerEp"]
        assert new_anime.total_days == total_days
        assert new_anime.total_hours == total_hours
        assert new_anime.source_data == SourceDataQueries(db_session).get_source_data_by_name(users_source.name)
        assert new_anime.active is False
        assert new_anime.synopsis is None
        assert new_anime.original_id == 0
        assert new_anime.related_media == []

        return new_anime

    def test_calculate_tfa_success(self, client, db_session, variables):
        response = self.request_api(
            query=self.query,
            test_client=client,
            variables=variables
        )

        self.assert_request_worked(response, variables, db_session)

    def test_calculate_tfa_with_already_existing_anime_anime(self, client, db_session, variables, anime):
        variables["title"] = anime.name

        response = self.request_api(
            query=self.query,
            test_client=client,
            variables=variables
        )

        anime = self.assert_request_worked(response, variables, db_session)

        assert anime.name_conflicts is True

    def test_calculate_tfa_with_invalid_name(self, client, variables):
        variables["title"] = " "

        self.assert_response_error(
            query=self.query,
            client=client,
            variables=variables,
            error_message="Title can't be blank."
        )

    def test_calculate_tfa_with_invalid_available_hours(self, client, variables):
        variables["availableHours"] = 0

        self.assert_response_error(
            query=self.query,
            client=client,
            variables=variables,
            error_message="Available hours must be have at least one minute."
        )

