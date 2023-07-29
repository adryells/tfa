from loguru import logger
from sqlalchemy.orm import Session

from app.data.size_type import size_types
from app.database.models.media.size_type import SizeType
from app.database.queries.request_change.size_type_queries import SizeTypeQueries


def load_size_types(session: Session):
    for size_type_data in size_types:

        size_type_exists = SizeTypeQueries(session).check_size_type_exists_with_name(name=size_type_data.name)

        if size_type_exists:
            logger.info(f"{size_type_data.name} syze type already exists. Skipping...")
            continue

        new_size_type = SizeType(
            name=size_type_data.name
        )

        session.add(new_size_type)
        session.flush()

        logger.info(f"{size_type_data.name} added.")

    session.commit()
