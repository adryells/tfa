from sqlalchemy import Column, Integer, String

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class SizeType(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String, nullable=False)

    slug = Column(String, nullable=False, unique=True)
