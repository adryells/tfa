from app.database.models.token.auth_token import AuthToken
from app.database.queries import BaseQueries


class AuthTokenQueries(BaseQueries):
    def get_active_auth_tokens_by_user_id(self, user_id: int) -> list[AuthToken]:
        auth_tokens = self.session.query(AuthToken).filter(AuthToken.user_id == user_id, AuthToken.active == True).all()

        return auth_tokens

    def get_auth_token_by_id(self, auth_token_id: int) -> AuthToken | None:
        auth_token = self.get_one_or_none_by_id(AuthToken, auth_token_id)

        return auth_token
