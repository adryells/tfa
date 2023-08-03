from app.database.models.role.basic import Role
from app.database.queries import BaseQueries
from app.database.models.permission.basic import Permission


class PermissionQueries(BaseQueries):

    def get_permissions_by_list_slug(self, list_slugs: list[str]) -> list[Permission]:
        permissions = self.session.query(Permission).filter(Permission.slug.in_(list_slugs)).all()

        return permissions

    def check_if_permission_exists_by_slug(self, slug: str) -> bool:
        exists = self.session.query(
            self.session.query(Permission.id).filter(Permission.slug == slug).exists()
        ).scalar()

        return exists

    def get_role_has_permission(self, role_id: int, permission_slug: str) -> bool:
        exists = self.session.query(
            self.session.query(Permission)
                .join(Role.permissions)
                .filter(Role.id == role_id, Permission.slug == permission_slug)
                .exists()
        ).scalar()

        return exists
