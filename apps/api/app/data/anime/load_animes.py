from faker import Faker
from loguru import logger
from sqlalchemy.orm import Session

from app.data.anime import animes
from app.data.size_type import medium, large
from app.database.queries.size_type_queries import SizeTypeQueries
from app.models.anime.basic import Anime
from app.models.media.basic import MediaItem

fake = Faker()


def generate_related_media(session: Session, anime: Anime) -> list[MediaItem]:
    medium_size_type = SizeTypeQueries(session).get_size_type_by_name(medium.name)
    large_size_type = SizeTypeQueries(session).get_size_type_by_name(large.name)

    media_items = []

    for size_type in [medium_size_type, large_size_type]:
        new_media_item = MediaItem(
            url=fake.image_url(),
            size_type=size_type,
            anime=anime
        )

        media_items.append(new_media_item)

        session.add(new_media_item)
        session.flush()

    return media_items


def load_anime_list(session: Session):
    for anime_data in animes:
        new_anime = Anime(
            name=anime_data.name,
            synopsis=anime_data.synopsis,
            num_episodes=anime_data.num_episodes,
            average_ep_duration=anime_data.average_ep_duration
        )

        session.add(new_anime)
        session.flush()

        medias = generate_related_media(session, new_anime)
        new_anime.related_media = medias

        logger.info(f"{anime_data.name} added.")

    session.commit()
