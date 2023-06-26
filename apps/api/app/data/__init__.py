from sqlalchemy.orm import Session

from app.data.anime.load_animes import load_anime_list
from app.data.size_type.load_size_types import load_size_types


def load_all_data(db_session: Session):
    load_size_types(db_session)
    load_anime_list(db_session)
