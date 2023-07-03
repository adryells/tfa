from graphene import ObjectType, List

from app.models.anime.basic import Anime
from app.services.types.generic import IdAsInt, PaginationData


class gAnime(IdAsInt):
    class Meta:
        model = Anime

    def resolve_total_hours(self: Anime, _):
        return round(self.total_hours, 2)

    def resolve_total_days(self: Anime, _):
        return round(self.total_days, 2)


class gAnimes(ObjectType, PaginationData):
    items = List(gAnime)
