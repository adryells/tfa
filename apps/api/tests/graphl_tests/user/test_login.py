from app.database.queries.auth_token.auth_token_queries import AuthTokenQueries
from tests import BaseTest


class TestLogin(BaseTest):
    query = """
        mutation ($password: String!, $email: String!){
          Login(inputLoginData: {email: $email, password: $password}){
            authToken{
              createdAt
              updatedAt
              token
              active
              id
              userId
              ipAddress
            }
          }
        }
    """

    def test_login_success(self, client, db_session, common_user):
        response = self.request_api(
            test_client=client,
            variables={"email": common_user.email, "password": "12345678"},
            query=self.query
        )

        assert response["data"]["Login"]["authToken"]

        auth_token_response = response["data"]["Login"]["authToken"]

        assert auth_token_response["id"]

        auth_token = AuthTokenQueries(db_session).get_auth_token_by_id(auth_token_id=auth_token_response["id"])

        assert auth_token_response["token"] == auth_token.token
        assert auth_token_response["ipAddress"] == auth_token.ip_address
        assert auth_token_response["userId"] == auth_token.user_id == common_user.id
        assert auth_token_response["active"] == auth_token.active == True

    def test_login_with_non_existent_user(self, client):
        self.assert_response_error(
            client=client,
            query=self.query,
            error_message="User not found.",
            variables={"password": "1234", "email": "tfa.tfa@tfa.tfa"}
        )

    def test_login_with_invalid_password(self, client, common_user):
        self.assert_response_error(
            client=client,
            variables={"email": common_user.email, "password": "12345677"},
            error_message="Password doesn't match.",
            query=self.query
        )
