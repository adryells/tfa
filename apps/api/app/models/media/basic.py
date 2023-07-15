from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class MediaItem(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    duration = Column(Integer)

    url = Column(String, nullable=False)

    title = Column(String, nullable=False)

    size = Column(String)

    mimetype = Column(String)

    active = Column(Boolean, default=True, nullable=False)

    public = Column(Boolean, default=True, nullable=False)

    media_type_id = Column(Integer, ForeignKey("mediatype.id"), nullable=False)
    media_type: 'MediaType' = relationship("MediaType", foreign_keys=[media_type_id])

    size_type_id = Column(Integer, ForeignKey("sizetype.id"), nullable=False)
    size_type: 'SizeType' = relationship("SizeType", foreign_keys=[size_type_id])

    creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    creator: 'User' = relationship("User", foreign_keys=[creator_id])
