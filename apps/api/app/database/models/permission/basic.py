from sqlalchemy import String, Column, Integer, Boolean
from sqlalchemy.orm import relationship

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class Permission(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String, nullable=False, unique=True)

    description = Column(String, nullable=False)

    active = Column(Boolean, nullable=False, default=True)

    roles: list['Role'] = relationship("Role", secondary="role_permissions", back_populates="permissions")
