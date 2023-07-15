import hashlib
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class AuthToken(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    token = Column(String, nullable=False, unique=True)

    ip_address = Column(String, nullable=False)

    active = Column(Boolean, default=True, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])

    def use(self):
        self.updated_at = datetime.now(timezone.utc)

    def generate(self):
        self.token = hashlib.sha256(str(uuid.uuid4()).encode("utf8")).hexdigest()

    def deactivate(self):
        self.active = False
