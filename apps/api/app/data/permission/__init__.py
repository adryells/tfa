from pydantic import BaseModel


class PermissionData(BaseModel):
    name: str
    description: str

    def __hash__(self):
        return hash((self.name, self.description))


get_users = PermissionData(
    name="Get users",
    description="Allows a user get info about users."
)

get_animes = PermissionData(
    name="Get animes",
    description="Allows a user get info about animes."
)

get_request_changes = PermissionData(
    name="Get request changes",
    description="Allows a user get info about request changes."
)

approve_request_changes = PermissionData(
    name="Approve request changes",
    description="Allows a user approve request changes."
)

update_anime_data = PermissionData(
    name="Update anime data",
    description="Allows a user update an anime."
)

update_user = PermissionData(
    name="Update user",
    description="Allows a user update self or another user."
)

create_user = PermissionData(
    name="Create user",
    description="Allows a user creation."
)

delete_user = PermissionData(
    name="Delete user",
    description="Allows a user deletion."
)

permission_datas = [
    get_users,
    get_animes,
    get_request_changes,
    approve_request_changes,
    update_anime_data,
    update_user,
    create_user,
    delete_user
]
