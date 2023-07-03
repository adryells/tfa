from sqlalchemy.orm import Session

from app.data.anime.load_animes import load_anime_list
from app.data.anime.load_from_files import load_real_anime_from_csv_files
from app.data.data.load_source_data import load_source_data
from app.data.size_type.load_size_types import load_size_types


def load_prod_data(db_session: Session):
    load_size_types(db_session)
    load_source_data(db_session)
    load_real_anime_from_csv_files(db_session)


def load_dev_data(db_session: Session):
    load_anime_list(db_session)


def load_all_data(db_session: Session):
    load_prod_data(db_session)
    load_dev_data(db_session)
