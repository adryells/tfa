from app.controllers import BaseController
from app.database.models.token.auth_token import AuthToken
from app.database.queries.auth_token.auth_token_queries import AuthTokenQueries
from app.database.queries.user.user_queries import UserQueries


class AuthTokenController(BaseController):
    def login(self, password: str, email: str, ip_address: str) -> AuthToken:
        user = UserQueries(self.session).get_user_by_email(email=email)

        if not user:
            raise Exception("User not found.")

        if not user.password_match(password):
            raise Exception("Password doesn't match.")

        self.deactivate_current_tokens(user_id=user.id)

        auth_token = self.create_auth_token(ip_address=ip_address, user_id=user.id)

        return auth_token

    def create_auth_token(self, ip_address: str, user_id: int) -> AuthToken:
        new_token = AuthToken(
            ip_address=ip_address,
            user_id=user_id
        ).generate().use()

        self.session.add(new_token)
        self.session.commit()

        return new_token

    def deactivate_current_tokens(self, user_id: int):
        auth_tokens = AuthTokenQueries(self.session).get_active_auth_tokens_by_user_id(user_id=user_id)

        for auth_token in auth_tokens:
            auth_token.deactivate()
            auth_token.delete()

        self.session.commit()
