from pydantic import BaseModel


class PermissionData(BaseModel):
    name: str
    slug: str
    description: str

    def __hash__(self):
        return hash((self.name, self.description))


get_users = PermissionData(
    name="Get users",
    description="Allows a user to get info about users.",
    slug="get_users"
)

get_animes = PermissionData(
    name="Get animes",
    description="Allows a user to get info about animes.",
    slug="get_animes"
)

get_request_changes = PermissionData(
    name="Get request changes",
    description="Allows a user to get info about request changes.",
    slug="get_request_changes"
)

update_anime_data = PermissionData(
    name="Update anime data",
    description="Allows a user to update an anime.",
    slug="update_anime_data"
)

update_user = PermissionData(
    name="Update user",
    description="Allows a user to update self or another user.",
    slug="update_user"
)

create_user = PermissionData(
    name="Create user",
    description="Allows a user creation.",
    slug="create_user"
)

delete_user = PermissionData(
    name="Delete user",
    description="Allows a user deletion.",
    slug="delete_user"
)

update_request_change = PermissionData(
    name="Update request change",
    description="Allows update an anime request change.",
    slug="update_request_change"
)

permission_datas = [
    get_users,
    get_animes,
    get_request_changes,
    update_anime_data,
    update_user,
    create_user,
    delete_user,
    update_request_change
]
