from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class Anime(DbBaseModel, CreatedUpdatedDeletedMixin):
    id: int = Column(Integer, primary_key=True, nullable=False)

    name: str = Column(String(80), nullable=False)

    related_media: list["MediaItem"] = relationship("MediaItem", backref="anime")

    synopsis: str = Column(String(300), nullable=False)

    num_episodes: int = Column(Integer, nullable=False)

    average_ep_duration: int = Column(Integer, nullable=False)
