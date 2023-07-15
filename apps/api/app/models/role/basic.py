from sqlalchemy import Column, Boolean, String, Integer
from sqlalchemy.orm import relationship

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class Role(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String, nullable=False, unique=True)

    description = Column(String, nullable=False)

    active = Column(Boolean, default=True, nullable=False)

    permissions: list['Permission'] = relationship("Permission", secondary="role_permissions", back_populates="roles")
