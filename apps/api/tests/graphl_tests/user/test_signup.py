import pytest

from app.data.role import common
from app.database.queries.role.role_queries import RoleQueries
from app.database.queries.user.user_queries import UserQueries
from app.utils.string_utils import INVALID_LENGTH, MISSING_NUMBERS, MISSING_CASE_LETTER, MISSING_SPECIAL_CHARACTERS
from tests import BaseTest
from tests.utils import format_date_graphql


class TestSignup(BaseTest):

    query = """
        mutation ($username: String!, $email: String!, $password: String!){
          Signup(inputSignupData: {
            username: $username,
            email: $email,
            password: $password
          }){
            user{
              createdAt
              updatedAt
              id
              username
              email
              active
              roleId
            }
          }
        }
    """

    @pytest.mark.parametrize("username", [" " * 4, "ab"])
    def test_signup_with_not_enough_characters(self, client, username):
        self.assert_response_error(
            client=client,
            variables={"username": username, "password": "12345678", "email": "ab@gmail.com"},
            query=self.query,
            error_message="Username's length must be a minimum of 3 characters."
        )

    @pytest.mark.parametrize("email", [
        "invalid_email@com", "john.doe@example", "no_at_symbol.com",
        "missing_domain@.com", "extra@dots..com", "adryell",
        "spaces in@email.com", "double@@symbol.com", "invalid#character.com"
    ])
    def test_signup_with_invalid_email(self, client, email):
        self.assert_response_error(
            client=client,
            error_message="Invalid Email.",
            query=self.query,
            variables={"username": "teste", "password": "12345678", "email": email}
        )

    @pytest.mark.parametrize("password, reason", [
        (" " * 4, INVALID_LENGTH),
        ("1234", INVALID_LENGTH),
        ("aaaaaaaa", MISSING_CASE_LETTER),
        ("AAAAAAAA", MISSING_CASE_LETTER),
        ("AaAaAaAa", MISSING_NUMBERS),
        ("AaAa12aA", MISSING_SPECIAL_CHARACTERS)
    ])
    def test_signup_with_invalid_password(self, client, password, reason):
        self.assert_response_error(
            client=client,
            variables={"email": "teste@tfa.tfa", "username": "teste", "password": password},
            query=self.query,
            error_message=reason
        )

    @pytest.mark.parametrize("variables, error_field", [
        (
            {"email": "teste@tfa.tfa", "password": "aAaAaA12"},
            "Variable '$username' of required type 'String!' was not provided."
        ),
        (
            {"password": "aAaAaA12", "username": "teste"},
            "Variable '$email' of required type 'String!' was not provided."
        ),
        (
            {"username": "aAaAaA12", "email": "teste@tfa.tfa"},
            "Variable '$password' of required type 'String!' was not provided."
        )
    ])
    def test_signup_missing_field(self, client, variables, error_field):
        self.assert_response_error(
            client=client,
            variables=variables,
            error_message=error_field,
            query=self.query
        )

    def test_signup_with_email_already_in_use(self, client, common_user):
        self.assert_response_error(
            client=client,
            query=self.query,
            variables={"email": common_user.email, "username": "tantofaz", "password": "@AaAaAa12"},
            error_message="Email already in use."
        )

    def test_signup_with_username_already_in_use(self, client, common_user):
        self.assert_response_error(
            client=client,
            query=self.query,
            variables={"email": "teste@tfa.tfa", "username": common_user.username, "password": "@AaAaAa12"},
            error_message="Username already in use."
        )

    def test_signup_success(self, client, db_session):
        variables = {
            "username": "Narutinho",
            "password": "#HinataÉmeuAmorOficiVr4U.",
            "email": "naruto@tfa.tfa"
        }

        response = self.request_api(
            client=client,
            variables=variables,
            query=self.query
        )

        assert not response.get("errors")

        assert response["data"]["Signup"]["user"]

        user_response = response["data"]["Signup"]["user"]

        assert user_response["id"]

        user = UserQueries(db_session).get_user_by_id(user_response["id"])
        role = RoleQueries(db_session).get_role_by_slug(common.slug)

        assert user_response["email"] == variables["email"] == user.email
        assert user_response["username"] == variables["username"] == user.username
        assert user_response["roleId"] == role.id == user.role_id
        assert user_response["updatedAt"] == user.updated_at
        assert user_response["createdAt"] == format_date_graphql(user.created_at)
        assert user_response["active"] == user.active == True
