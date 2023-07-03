from faker import Faker
from loguru import logger
from sqlalchemy.orm import Session

from app.data.anime import animes
from app.data.data import imagination_source
from app.data.size_type import medium, large
from app.database.queries.size_type_queries import SizeTypeQueries
from app.models.anime.basic import Anime
from app.models.media.basic import MediaItem
from app.queries.source_data.source_data_queries import SourceDataQueries

fake = Faker()


def generate_related_media(session: Session, anime: Anime, medium_url: str = None, large_url: str = None) -> list[MediaItem]:
    medium_size_type = SizeTypeQueries(session).get_size_type_by_name(medium.name)
    large_size_type = SizeTypeQueries(session).get_size_type_by_name(large.name)

    media_items = []

    for size_type in [medium_size_type, large_size_type]:
        param_url = medium_url if size_type.name == medium.name else large_url
        url = param_url or fake.image_url()

        new_media_item = MediaItem(
            url=url,
            size_type=size_type,
            anime=anime
        )

        media_items.append(new_media_item)

        session.add(new_media_item)
        session.flush()

    return media_items


def load_anime_list(session: Session):
    source_data = SourceDataQueries(session).get_source_data_by_name(name=imagination_source.name)

    for anime_data in animes:
        new_anime = Anime(
            name=anime_data.name,
            synopsis=anime_data.synopsis,
            num_episodes=anime_data.num_episodes,
            average_ep_duration=anime_data.average_ep_duration,
            source_data=source_data,
            original_id=0
        )

        session.add(new_anime)
        session.flush()

        medias = generate_related_media(session, new_anime)
        new_anime.related_media = medias

        logger.info(f"{anime_data.name} added.")

    session.commit()
