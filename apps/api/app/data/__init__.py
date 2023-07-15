from sqlalchemy.orm import Session

from app.data.anime.load_animes import load_anime_list
from app.data.anime.load_from_files import load_real_anime_from_csv_files
from app.data.data.load_source_data import load_source_data
from app.data.media_type.load_media_types import load_media_types
from app.data.permission.load_permissions import load_permissions
from app.data.role.load_roles import load_roles
from app.data.size_type.load_size_types import load_size_types
from app.data.user import dev_users, prod_users
from app.data.user.load_users import load_users


def load_prod_data(db_session: Session, real_anime: bool = False):
    load_size_types(db_session)
    load_source_data(db_session)
    load_media_types(db_session)
    load_permissions(db_session)
    load_roles(db_session)
    load_users(db_session, user_datas=prod_users)

    if real_anime:
        load_real_anime_from_csv_files(db_session)


def load_dev_data(db_session: Session):
    load_anime_list(db_session)
    load_users(db_session, user_datas=dev_users)


def load_all_data(db_session: Session):
    load_prod_data(db_session)
    load_dev_data(db_session)
