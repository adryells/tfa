from tests import BaseTest


class TestGetOneAnime(BaseTest):
    query = """
        query getAnime($animeId: Int!){
          Animes{
            anime(animeId: $animeId){
              createdAt
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
            }
          }
        }
    """

    def test_get_one_anime_success(self, client, anime):
        response = self.request_api(
            client=client,
            variables={"animeId": anime.id},
            query=self.query
        )

        assert response["data"]["Animes"]["anime"]

        anime_response = response["data"]["Animes"]["anime"]

        assert anime_response["id"] == anime.id
        assert anime_response["name"] == anime.name
        assert anime_response["active"] == anime.active
        assert anime_response["synopsis"] == anime.synopsis
        assert anime_response["totalDays"] == round(anime.total_days, 2)
        assert anime_response["totalHours"] == round(anime.total_hours, 2)
        assert anime_response["numEpisodes"] == anime.num_episodes
        assert anime_response["sourceDataId"] == anime.source_data_id
        assert anime_response["nameConflicts"] == anime.name_conflicts
        assert anime_response["averageEpDuration"] == anime.average_ep_duration

    def test_get_invalid_anime(self, client):
        self.assert_response_error(
            client=client,
            query=self.query,
            variables={"animeId": 1000},
            error_message="Anime not found."
        )
