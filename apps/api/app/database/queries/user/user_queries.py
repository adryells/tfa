from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Query

from app.database.models.token.auth_token import AuthToken
from app.database.queries import BaseQueries
from app.database.models.role.basic import Role
from app.database.models.user.basic import User


class UserQueries(BaseQueries):
    def check_user_exists_by_username(self, username: str) -> bool:
        exists = self.session.query(
            self.session.query(User.username).filter(func.lower(User.username) == username.lower()).exists()
        ).scalar()

        return exists

    def get_user_by_username(self, username: str) -> Optional[User]:
        user = self.session.query(User).filter(func.lower(User.username) == username.lower()).one_or_none()

        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        user = self.session.query(User).filter(User.id == user_id).one_or_none()

        return user

    def user_has_role(self, role_slug: str, user_id: int) -> bool:
        exists = self.session.query(
            self.session.query(User.role).join(User.role).filter(Role.slug == role_slug, User.id == user_id).exists()
        ).scalar()

        return exists

    def check_user_exists_by_email(self, email: str) -> bool:
        exists = self.session.query(
            self.session.query(User.email).filter(func.lower(User.email) == email.lower()).exists()
        ).scalar()

        return exists

    def get_users(self, page: int, per_page: int, search: str) -> list[User]:
        query = self._get_users_query(search=search)

        if page and per_page:
            query = self.get_query_with_pagination(query, page, per_page)

        return query

    def _get_users_query(self, search: str) -> Query:
        query = self.session.query(User)

        if search:
            query = query.filter(User.username.ilike(f"%{search}%"))

        return query

    def get_users_count(self, search: str) -> int:
        query = self._get_users_query(search=search)

        return query.count()

    def get_user_by_email(self, email: str) -> Optional[User]:
        user = self.session.query(User).filter(func.lower(User.email) == email.lower()).one_or_none()

        return user

    def get_user_by_token(self, token: str) -> User:
        user = self.session.query(User)\
            .join(AuthToken)\
            .filter(AuthToken.active == True, AuthToken.token == token)\
            .first()

        return user
