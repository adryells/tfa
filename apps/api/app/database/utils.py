from sqlalchemy.orm import Session

from apps.api.app.database.base_class import DbBaseModel


def init_db(db_session: Session):
    DbBaseModel.metadata.create_all(bind=db_session.bind)


def drop_db(db_session: Session):
    DbBaseModel.metadata.drop_all(bind=db_session.bind)
