from sqlalchemy import Integer, Column, String, ForeignKey, Boolean, Float
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.database.base_class import DbBaseModel
from app.database.mixins import CreatedUpdatedDeletedMixin
from app.database.models.data.basic import SourceData


class Anime(DbBaseModel, CreatedUpdatedDeletedMixin):
    id = Column(Integer, primary_key=True, nullable=False)

    original_id = Column(Integer, nullable=False, default=0)

    name = Column(String, nullable=False)

    related_media: list["MediaItem"] = relationship("MediaItem", secondary="anime_medias")

    synopsis = Column(String)

    num_episodes = Column(Integer, nullable=False)

    average_ep_duration = Column(Float, nullable=False)

    source_data_id = Column(Integer, ForeignKey(SourceData.id), nullable=False)
    source_data: SourceData = relationship(SourceData, foreign_keys=[source_data_id])

    active = Column(Boolean, nullable=False, default=True)

    name_conflicts = Column(Boolean, nullable=False, default=False)

    @hybrid_property
    def total_hours(self) -> float:
        calc = (self.average_ep_duration * self.num_episodes) / 60

        return calc

    @hybrid_property
    def total_days(self) -> float:
        calc = self.total_hours / 24

        return calc

    def to_dict(self):
        return {
            "id": self.id,
            "original_id": self.original_id,
            "name": self.name,
            "synopsis": self.synopsis,
            "num_episodes": self.num_episodes,
            "average_ep_duration": self.average_ep_duration,
            "source_data_id": self.source_data_id,
            "active": self.active,
            "name_conflicts": self.name_conflicts
        }
