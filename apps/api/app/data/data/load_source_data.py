from loguru import logger
from sqlalchemy.orm import Session

from app.data.data import sources
from app.database.models.data.basic import SourceData
from app.database.queries.source_data.source_data_queries import SourceDataQueries


def load_source_data(session: Session):

    for source_data in sources:
        existing_source_data = SourceDataQueries(session).check_source_data_exists_with_slug(slug=source_data.name)

        if existing_source_data:
            logger.info(f"Source data: {source_data.name} found. Skipping...")
            continue

        new_source_data = SourceData(
            name=source_data.name,
            slug=source_data.slug
        )

        session.add(new_source_data)
        session.commit()
