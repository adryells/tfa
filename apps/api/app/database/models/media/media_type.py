from sqlalchemy import Column, Integer, String, Boolean

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class MediaType(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String, nullable=False)

    active = Column(Boolean, nullable=False, default=True)
