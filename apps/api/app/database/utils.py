from sqlalchemy.orm import Session

from app.data import load_all_data
from app.database.base_class import DbBaseModel


def init_db(db_session: Session):
    DbBaseModel.metadata.create_all(bind=db_session.bind)


def drop_db(db_session: Session):
    DbBaseModel.metadata.drop_all(bind=db_session.bind)


def restart_db(db_session: Session, drop: bool = True, load: bool = True, create: bool = True):
    if drop:
        drop_db(db_session)

    if create:
        init_db(db_session)

    if load:
        load_all_data(db_session)
