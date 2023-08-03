from loguru import logger
from sqlalchemy.orm import Session

from app.data.user import UserData
from app.database.models.user.basic import User
from app.database.queries.role.role_queries import RoleQueries
from app.database.queries.user.user_queries import UserQueries


def load_users(session: Session, user_datas: list[UserData]):
    for user_data in user_datas:
        existing_user = UserQueries(session).check_user_exists_by_username(user_data.username)

        if existing_user:
            logger.info(f"User {user_data.username} already exists. Skipping...")
            continue

        role = RoleQueries(session).get_role_by_slug(user_data.role.slug)

        user = User(
            email=user_data.email,
            username=user_data.username,
            role=role
        ).set_password("12345678")

        session.add(user)
        session.commit()

        logger.info(f"User {user_data.username} added.")
