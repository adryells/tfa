from sqlalchemy.orm import Query

from app.database.queries import BaseQueries
from app.database.models.role.basic import Role
from app.database.models.user.basic import User


class UserQueries(BaseQueries):
    def check_user_exists_by_username(self, username: str) -> bool:
        exists = self.session.query(
            self.session.query(User.username).filter(User.username == username).exists()
        ).scalar()

        return exists

    def get_user_by_username(self, username: str) -> User | None:
        user = self.session.query(User).filter(User.username == username).one_or_none()

        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.session.query(User).filter(User.id == user_id).one_or_none()

        return user

    def user_has_role(self, role_name: str, user_id: int) -> bool:
        exists = self.session.query(
            self.session.query(User.role).join(User.role) .filter(Role.name == role_name, User.id == user_id).exists()
        ).scalar()

        return exists

    def check_user_exists_by_email(self, email: str) -> bool:
        exists = self.session.query(
            self.session.query(User.email).filter(User.email == email).exists()
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

    def get_user_by_email(self, email: str) -> User | None:
        user = self.session.query(User).filter(User.email == email).one_or_none()

        return user
