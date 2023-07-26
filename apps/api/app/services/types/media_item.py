from app.database.models.media.basic import MediaItem
from app.services.types.generic import IdAsInt


class gMediaItem(IdAsInt):
    class Meta:
        model = MediaItem
