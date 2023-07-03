from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class MediaItem(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    url = Column(String, nullable=False)

    anime_id = Column(Integer, ForeignKey("anime.id"), nullable=False)

    size_type_id = Column(Integer, ForeignKey("sizetype.id"), nullable=False)
    size_type: 'SizeType' = relationship("SizeType", foreign_keys=[size_type_id])
