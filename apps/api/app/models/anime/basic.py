from sqlalchemy import Integer, Column, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin


class Anime(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String(80), nullable=False)

    related_media: list["MediaItem"] = relationship("MediaItem", backref="anime")

    synopsis = Column(String(300), nullable=False)

    num_episodes = Column(Integer, nullable=False)

    average_ep_duration = Column(Integer, nullable=False)

    @hybrid_property
    def total_hours(self) -> float:
        calc = self.average_ep_duration * self.num_episodes

        return calc

    @hybrid_property
    def total_days(self) -> float:
        calc = self.total_hours / 24

        return calc
