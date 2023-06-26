import requests

client_id = ""
client_secret = ""

base_url = "https://api.myanimelist.net/v2"

field_path_params = "?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"


headers = {
    "X-MAL-CLIENT-ID": client_id,
}


def get_anime_by_id(anime_id: int):
    url = base_url + f"/anime/{anime_id}" + field_path_params
    requests.get(url, headers=headers)


get_anime_by_id(anime_id=1)
