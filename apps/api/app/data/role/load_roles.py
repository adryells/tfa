from loguru import logger
from sqlalchemy.orm import Session

from app.data.role import role_datas
from app.database.models.role.basic import Role
from app.database.queries.permission.permission_queries import PermissionQueries
from app.database.queries.role.role_queries import RoleQueries


def load_roles(session: Session):
    for role_data in role_datas:
        existing_role = RoleQueries(session).check_if_role_exists_by_name(role_data.name)

        if existing_role:
            logger.info(f"Role {role_data.name} already exists. Skipping...")
            continue

        role = Role(
            name=role_data.name,
            description=role_data.description
        )

        list_name = [permission.name for permission in role_data.permissions]

        permissions = PermissionQueries(session).get_permissions_by_list_name(list_name)

        role.permissions = permissions

        session.add(role)
        session.commit()

        logger.info(f"Role {role_data.name} added.")
