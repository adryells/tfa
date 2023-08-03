from datetime import datetime

import pytest
from faker import Faker

from app.data.size_type import large
from app.database.queries.anime.anime_queries import AnimeQueries
from app.database.queries.request_change.size_type_queries import SizeTypeQueries
from tests import BaseTest
from tests.utils import format_date_graphql


class TestUpdateAnime(BaseTest):
    query = """
        mutation (
          $anime_id: Int!,
          $name: String,
          $synopsis: String,
          $num_episodes: Int,
          $average_ep_duration: Int,
          $active: Boolean,
          $source_data_id: Int,
          $medium_image_id: Int,
          $large_image_id: Int,
          $request_change_id: Int
        ){
          UpdateAnime(inputUpdateAnimeData:{
            animeId: $anime_id,
            name: $name,
            synopsis: $synopsis,
            numEpisodes: $num_episodes,
            averageEpDuration: $average_ep_duration,
            sourceDataId: $source_data_id,
            active: $active,
            mediumImageId: $medium_image_id,
            largeImageId: $large_image_id,
            requestChangeId: $request_change_id
          }){
            anime{
              createdAt
              updatedAt
              id
              originalId
              name
              synopsis
              numEpisodes
              averageEpDuration
              sourceDataId
              active
              nameConflicts
              totalHours
              totalDays
              relatedMedia{
                id
                url
                title
                public
                active
                mediaTypeId
                sizeTypeId
                creatorId
              }
            }
          }
        }
    """

    fake = Faker()

    def _assert_anime_response_success(
            self,
            anime_id: int,
            created_at: datetime,
            updated_at: datetime,
            original_id: int,
            num_episodes_request: int,
            num_episodes_db: int,
            name_conflicts: bool,
            total_hours: int,
            total_days: int,
            name_request: str,
            name_db: str,
            synopsis_request: str,
            synopsis_db: str,
            average_ep_duration_request: int,
            average_ep_duration_db: int,
            source_data_id_request: int,
            source_data_id_db: int,
            active_request: bool,
            active_db: bool,
            response: dict
    ):
        assert response["id"] == anime_id
        assert response["createdAt"] == format_date_graphql(str(created_at))
        assert response["updatedAt"] == format_date_graphql(str(updated_at))
        assert response["originalId"] == original_id
        assert response["numEpisodes"] == num_episodes_request == num_episodes_db
        assert response["name"] == name_request == name_db
        assert response["synopsis"] == synopsis_request == synopsis_db
        assert response["averageEpDuration"] == average_ep_duration_request == average_ep_duration_db
        assert response["sourceDataId"] == source_data_id_request == source_data_id_db
        assert response["active"] == active_request == active_db
        assert response["nameConflicts"] == name_conflicts
        assert response["totalHours"] == round(total_hours, 2)
        assert response["totalDays"] == round(total_days, 2)

    def _get_variables(
            self,
            anime_id: int = 1,
            name: str = fake.pystr(),
            synopsis: str = fake.pystr(),
            num_episodes: int = fake.pyint(),
            average_ep_duration: int = fake.pyint(),
            source_data_id: int = 3,
            active: bool = False,
            medium_image_id: int = 1,
            large_image_id: int = 2
    ) -> dict:
        return {
            "anime_id": anime_id,
            "name": name,
            "synopsis": synopsis,
            "num_episodes": num_episodes,
            "average_ep_duration": average_ep_duration,
            "source_data_id": source_data_id,
            "active": active,
            "medium_image_id": medium_image_id,
            "large_image_id": large_image_id
        }

    def test_update_anime_success(
            self,
            client,
            db_session,
            admin_auth_token,
            request_change,
            anime,
            anime_picture_media,
            large_anime_picture_media
    ):
        variables = self._get_variables(
            medium_image_id=anime_picture_media.id,
            large_image_id=large_anime_picture_media.id
        )

        response = self.request_api(
            client=client,
            variables=variables,
            token=admin_auth_token.token,
            query=self.query
        )

        assert not response.get("errors")

        assert response["data"]["UpdateAnime"]["anime"]

        anime_response = response["data"]["UpdateAnime"]["anime"]
        anime_db = AnimeQueries(db_session).get_anime_by_id(variables["anime_id"])

        self._assert_anime_response_success(
            anime_id=variables["anime_id"],
            created_at=anime_db.created_at,
            updated_at=anime_db.updated_at,
            original_id=anime_db.original_id,
            num_episodes_db=anime_db.num_episodes,
            num_episodes_request=variables["num_episodes"],
            name_request=variables["name"],
            name_db=anime_db.name,
            name_conflicts=anime_db.name_conflicts,
            total_days=anime_db.total_days,
            total_hours=anime_db.total_hours,
            active_request=variables["active"],
            active_db=anime_db.active,
            synopsis_request=variables["synopsis"],
            synopsis_db=anime_db.synopsis,
            average_ep_duration_db=anime_db.average_ep_duration,
            average_ep_duration_request=variables["average_ep_duration"],
            source_data_id_request=variables["source_data_id"],
            source_data_id_db=anime_db.source_data_id,
            response=anime_response
        )

    def test_update_anime_with_request_change_values(
            self,
            client,
            db_session,
            admin_auth_token,
            request_change,
            anime,
            anime_picture_media,
            large_anime_picture_media
    ):
        variables = self._get_variables(
            medium_image_id=anime_picture_media.id,
            large_image_id=large_anime_picture_media.id
        )

        variables["request_change_id"] = request_change.id

        response = self.request_api(
            client=client,
            variables=variables,
            token=admin_auth_token.token,
            query=self.query
        )

        assert not response.get("errors")
        assert response["data"]["UpdateAnime"]["anime"]

        anime_response = response["data"]["UpdateAnime"]["anime"]
        anime_db = AnimeQueries(db_session).get_anime_by_id(variables["anime_id"])

        request_change_data = request_change.change_data

        self._assert_anime_response_success(
            anime_id=variables["anime_id"],
            created_at=anime_db.created_at,
            updated_at=anime_db.updated_at,
            original_id=anime_db.original_id,
            num_episodes_db=anime_db.num_episodes,
            num_episodes_request=request_change_data["num_episodes"],
            name_request=request_change_data["name"],
            name_db=anime_db.name,
            name_conflicts=anime_db.name_conflicts,
            total_days=anime_db.total_days,
            total_hours=anime_db.total_hours,
            active_request=request_change_data["active"],
            active_db=anime_db.active,
            synopsis_request=request_change_data["synopsis"],
            synopsis_db=anime_db.synopsis,
            average_ep_duration_db=anime_db.average_ep_duration,
            average_ep_duration_request=request_change_data["average_ep_duration"],
            source_data_id_request=variables["source_data_id"],
            source_data_id_db=anime_db.source_data_id,
            response=anime_response
        )

    def test_update_anime_with_non_existent_anime(self, client, admin_auth_token, anime):
        self.assert_response_error(
            query=self.query,
            client=client,
            variables=self._get_variables(anime_id=1000),
            token=admin_auth_token.token,
            error_message="Anime not found."
        )

    @pytest.mark.parametrize("field", ["medium_image_id", "large_image_id"])
    def test_update_anime_with_invalid_media_type(self, client, db_session, admin_auth_token, profile_picture_media, field, anime):
        variables = self._get_variables()
        variables[field] = profile_picture_media.id

        self.assert_response_error(
            client=client,
            query=self.query,
            variables=variables,
            error_message="Wrong media type.",
            token=admin_auth_token.token
        )

    @pytest.mark.parametrize("field", ["medium_image_id", "large_image_id"])
    def test_update_anime_with_invalid_size_type(self, client, db_session, admin_auth_token, anime_picture_media, field, anime):
        variables = self._get_variables()
        variables[field] = anime_picture_media.id

        if field == "medium_image_id":
            anime_picture_media.size_type = SizeTypeQueries(db_session).get_size_type_by_slug(large.slug)
            db_session.commit()

        self.assert_response_error(
            client=client,
            query=self.query,
            variables=variables,
            error_message="Wrong size type.",
            token=admin_auth_token.token
        )

    def test_update_anime_with_non_existent_request_change(self, client, admin_auth_token, anime):
        variables = self._get_variables()
        variables["request_change_id"] = 1000

        self.assert_response_error(
            error_message="Request change not found.",
            variables=variables,
            token=admin_auth_token.token,
            client=client,
            query=self.query
        )
