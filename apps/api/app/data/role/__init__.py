from pydantic import BaseModel

from app.data.permission import PermissionData, permission_datas, get_request_changes, approve_request_changes, \
    update_anime_data, update_request_change, delete_user, create_user

all_permissions = permission_datas


class RoleData(BaseModel):
    name: str
    description: str
    excluded: list[PermissionData] = []

    def __hash__(self):
        return hash((self.name, self.description))

    @property
    def permissions(self):
        return list(set(all_permissions) - set(self.excluded))


admin = RoleData(
    name="Admin",
    description="System's god"
)


common = RoleData(
    name="Common",
    description="A simple user with basic permissions for some read/write actions.",
    excluded=[
        get_request_changes,
        update_anime_data,
        update_request_change,
        delete_user,
        create_user
    ]
)

role_datas = [
    admin,
    common
]
