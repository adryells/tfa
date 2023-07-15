from app.database.queries import BaseQueries
from app.models.role.basic import Role


class RoleQueries(BaseQueries):

    def check_if_role_exists_by_name(self, name: str) -> bool:
        exists = self.session.query(
            self.session.query(Role).filter(Role.name == name).exists()
        ).scalar()

        return exists

    def get_role_by_name(self, name: str) -> Role | None:
        role = self.session.query(Role).filter(Role.name == name).one_or_none()

        return role
