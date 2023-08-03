from loguru import logger
from sqlalchemy.orm import Session

from app.data.permission import permission_datas
from app.database.models.permission.basic import Permission
from app.database.queries.permission.permission_queries import PermissionQueries


def load_permissions(session: Session):
    for permission_data in permission_datas:
        existing_permission = PermissionQueries(session).check_if_permission_exists_by_slug(permission_data.slug)

        if existing_permission:
            logger.info(f"Permission {permission_data.name} already exists. Skipping...")
            continue

        permission = Permission(
            name=permission_data.name,
            slug=permission_data.slug,
            description=permission_data.description
        )

        session.add(permission)
        session.commit()

        logger.info(f"Permission {permission_data.name} added.")
