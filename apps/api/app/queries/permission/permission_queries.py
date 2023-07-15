from app.database.queries import BaseQueries
from app.models.permission.basic import Permission


class PermissionQueries(BaseQueries):

    def get_permissions_by_list_name(self, list_name: list[str]) -> list[Permission]:
        permissions = self.session.query(Permission).filter(Permission.name.in_(list_name)).all()

        return permissions

    def check_if_permission_exists_by_name(self, name: str) -> bool:
        exists = self.session.query(
            self.session.query(Permission.id).filter(Permission.name == name).exists()
        ).scalar()

        return exists
