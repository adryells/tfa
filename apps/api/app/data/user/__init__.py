from pydantic import BaseModel

from app.data.role import RoleData, admin as admin_role, common


class UserData(BaseModel):
    username: str
    email: str
    role: RoleData


admin = UserData(
    username="tfa_admin",
    email="tfa_admin@tfa.tfa",
    role=admin_role
)

adryell = UserData(
    username="adryell",
    email="adryell@tfa.tfa",
    role=common
)

jaw = UserData(
    username="jaw",
    email="jaw@tfa.tfa",
    role=common
)

roger = UserData(
    username="roger",
    email="roger@tfa.tfa",
    role=common
)

jhonny = UserData(
    username="jhonny",
    email="jhonny@tfa.tfa",
    role=common
)

caduestest = UserData(
    username="caduestest",
    email="cadu@tfa.tfa",
    role=common
)

dev_users = [
    adryell,
    jaw,
    roger,
    jhonny,
    caduestest
]

prod_users = [
    admin
]

