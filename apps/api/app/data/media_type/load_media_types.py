from loguru import logger
from sqlalchemy.orm import Session

from app.data.media_type import media_type_datas
from app.database.models.media.media_type import MediaType
from app.database.queries.media_type.media_type_queries import MediaTypeQueries


def load_media_types(session: Session):
    for media_type_datum in media_type_datas:
        existing_media_type = MediaTypeQueries(session).check_if_media_type_exists_by_slug(media_type_datum.slug)

        if existing_media_type:
            logger.info(f"Media type {media_type_datum.name} already exists. Skipping...")
            continue

        media_type = MediaType(
            name=media_type_datum.name,
            slug=media_type_datum.slug
        )

        session.add(media_type)
        session.commit()

        logger.info(f"media type {media_type_datum.name} added.")
