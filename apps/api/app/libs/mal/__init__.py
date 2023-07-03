import requests

from app.config import settings


class MalAPI:
    def __init__(self, base_url: str = None, client_secret: str = None, client_id: str = None):
        self.base_url = base_url or settings.MAL_BASE_URL
        self.client_secret = client_secret or settings.MAL_CLIENT_SECRET
        self.field_path_params = "?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"
        self.headers = {
            # 'Content-Type': 'application/json',
            "X-MAL-CLIENT-ID": client_id or settings.MAL_CLIENT_ID
        }

    def get_anime_by_id(self, anime_id: int):
        url = self.base_url + f"/anime/{anime_id}" + self.field_path_params

        response = requests.get(url, headers=self.headers)

        return response.json()

    def get_animes_by_season(self, year: int, season: str, limit: int):
        url = self.base_url + f"/anime/season/{year}/{season}" + self.field_path_params + f"&limit={limit}"

        response = requests.get(url, headers=self.headers)

        return response.json()
