import csv

from app.libs.mal import MalAPI
from app.utils.enums import SeasonEnum

mal_api = MalAPI()


def generate_file_data(season: str, year: int):
    response = mal_api.get_animes_by_season(year=year, season=season, limit=500)

    with open(f"{season}_{year}.csv", "a+", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(response["data"])


if __name__ == "__main__":
    for year in list(range(2001, 2024)):
        for season in SeasonEnum:
            generate_file_data(year=year, season=season.value)
