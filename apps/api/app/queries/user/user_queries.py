from app.database.queries import BaseQueries
from app.models.user.basic import User


class UserQueries(BaseQueries):
    def check_user_exists_by_username(self, username: str) -> bool:
        exists = self.session.query(
            self.session.query(User.username).filter(User.username == username).exists()
        ).scalar()

        return exists

    def get_user_by_username(self, username: str) -> User | None:
        user = self.session.query(User).filter(User.username == username).one_or_none()

        return user
