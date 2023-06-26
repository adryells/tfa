from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from app.config import settings

engine = create_engine(url=settings.DATABASE_URL, poolclass=NullPool)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session() -> Iterator[Session]:
    db_session = SessionLocal()

    yield db_session

    db_session.close()


def main_session() -> Session:
    return next(get_session())
