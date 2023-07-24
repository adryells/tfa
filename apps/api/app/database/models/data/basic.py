from sqlalchemy import Column, Integer, String

from app.database.base_class import DbBaseModel


class SourceData(DbBaseModel):
    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String, nullable=False)
