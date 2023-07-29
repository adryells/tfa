import hashlib
import os

from sqlalchemy import Integer, Column, String, Boolean, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class User(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    username = Column(String, nullable=False, unique=True)

    email = Column(String, nullable=False, unique=True)

    password = Column(LargeBinary, nullable=False)

    password_salt = Column(LargeBinary, nullable=False)

    active = Column(Boolean, default=True, nullable=False)

    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    role: 'Role' = relationship("Role", foreign_keys=[role_id]) # noqa

    related_media = relationship("MediaItem", secondary="user_medias")

    def set_password(self, password: str):
        self.password_salt = os.urandom(32)
        self.password = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode('utf-8'),
            salt=self.password_salt,
            iterations=122381,
            dklen=128
        )

        return self

    def password_match(self, password) -> bool:
        return hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode('utf-8'),
            salt=self.password_salt,
            iterations=122381,
            dklen=128
        ) == self.password

    def profile_picture(self) -> "MediaItem": # noqa
        for media in self.related_media:
            if media.media_type.name == "Profile Picture":
                return media
