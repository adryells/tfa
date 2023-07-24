from app.database.models.token.auth_token import AuthToken
from app.services.types.generic import IdAsInt


class gAuthToken(IdAsInt):
    class Meta:
        model = AuthToken
