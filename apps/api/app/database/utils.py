from sqlalchemy.orm import Session

from app.data import load_all_data
from app.database.base_class import DbBaseModel
from app.database.session import main_session


def init_db(db_session: Session):
    DbBaseModel.metadata.create_all(bind=db_session.bind)


def drop_db(db_session: Session):
    DbBaseModel.metadata.drop_all(bind=db_session.bind)


def restart_db(db_session: Session):
    drop_db(db_session)
    init_db(db_session)
    load_all_data(db_session)


restart_db(main_session())
