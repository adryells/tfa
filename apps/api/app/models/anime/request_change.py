from sqlalchemy import Integer, Column, JSON, String, Boolean, ForeignKey
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class RequestChange(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    change_data = Column(MutableDict.as_mutable(JSON), nullable=False)

    reason = Column(String, nullable=False)

    additional_info = Column(String)

    active = Column(Boolean, nullable=False, default=True)

    accepted = Column(Boolean, nullable=False, default=False)

    anime_id = Column(Integer, ForeignKey("anime.id"), nullable=False)
    anime: 'Anime' = relationship("Anime", foreign_keys=[anime_id])
