from app.database.mixins import create_linking_table
from app.models.anime.basic import Anime
from app.models.media.basic import MediaItem
from app.models.permission.basic import Permission
from app.models.role.basic import Role
from app.models.user.basic import User

user_medias = create_linking_table(User, MediaItem, table_name="user_medias")

anime_medias = create_linking_table(Anime, MediaItem, table_name="anime_medias")

role_permissions = create_linking_table(Role, Permission, table_name="role_permissions")
