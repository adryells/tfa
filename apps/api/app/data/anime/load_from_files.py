import csv
import os

from loguru import logger
from sqlalchemy.orm import Session

from app.data.anime.load_animes import generate_related_media
from app.data.data import mal_source
from app.database.queries.source_data.source_data_queries import SourceDataQueries
from app.database.session import main_session
from app.libs.mal import MalAPI
from app.database.models.anime.basic import Anime
from app.database.queries.anime.anime_queries import AnimeQueries

mal_api = MalAPI()


def load_real_anime_from_csv_files(session: Session):
        folders = os.path.join(os.getcwd(), r"app\data\anime\anime_data")

        for folder in os.listdir(folders):
            absolute_path_folder = os.path.join(folders, folder)
            files = os.listdir(absolute_path_folder)

            logger.info(f"Loading {folder} data...")

            for file in files:

                with open(os.path.join(absolute_path_folder, file), "r+", encoding="utf-8") as csv_file:
                    reader = csv.reader(csv_file)
                    source_data = SourceDataQueries(session).get_source_data_by_name(name=mal_source.name)

                    for index, row in enumerate(reader, start=1):
                        for item in row:
                            item_node = eval(item)["node"]

                            existing_anime = AnimeQueries(session).check_anime_exists_with_name(name=item_node["title"])

                            if existing_anime:
                                logger.info(f"Anime {item_node['title']} already registered. Skipping...")
                                continue

                            new_anime = Anime(
                                original_id=item_node["id"],
                                name=item_node["title"],
                                synopsis=item_node["synopsis"],
                                num_episodes=item_node["num_episodes"],
                                average_ep_duration=item_node["average_episode_duration"],
                                source_data=source_data
                            )

                            session.add(new_anime)
                            session.flush()

                            logger.info(f"{new_anime.name} added.")

                            if item_node.get("main_picture"):
                                medium_url = item_node["main_picture"]["medium"]
                                large_url = item_node["main_picture"]["large"]

                            generate_related_media(session, new_anime, medium_url, large_url)

                    session.commit()


if __name__ == "__main__":
    load_real_anime_from_csv_files(session=main_session())
