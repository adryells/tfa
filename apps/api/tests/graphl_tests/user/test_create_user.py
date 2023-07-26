from random import choice

import pytest

from app.database.queries.user.user_queries import UserQueries
from app.utils.string_utils import MISSING_NUMBERS, MISSING_SPECIAL_CHARACTERS, INVALID_LENGTH, MISSING_CASE_LETTER
from tests import BaseTest


class TestCreateUser(BaseTest):
    query = """
        mutation createUser(
          $username: String!, 
          $active: Boolean,
          $password: String!,
          $roleId: Int!,
          $profilePictureId: Int!,
          $email: String!
        ){
          CreateUser(inputCreateUserData:{
            username: $username,
            email: $email,
            roleId: $roleId,
            profilePictureId: $profilePictureId,
            active: $active,
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
              profilePicture{
                id
              }
            }
          }
        }
    """

    def _get_variables(
            self,
            profile_picture_id: int = 1,
            username: str = "Clotilde",
            email: str = "clotilde@tfa.tfa",
            active: bool = choice([True, False]),
            password: str = "@AaAaAa12",
            role_id: int = 1
    ) -> dict:
        return {
            "username": username,
            "email": email,
            "password": password,
            "profilePictureId": profile_picture_id,
            "roleId": role_id,
            "active": active
        }

    def test_create_user_success(self, client, db_session, profile_picture_media):
        variables = self._get_variables()

        response = self.request_api(
            test_client=client,
            variables=variables,
            query=self.query
        )

        assert not response.get("errors")

        assert response["data"]["CreateUser"]["user"]

        user_response = response["data"]["CreateUser"]["user"]

        assert user_response["id"]

        user = UserQueries(db_session).get_user_by_id(user_response["id"])

        assert user.password_match(variables["password"])

        assert user_response["email"] == variables["email"] == user.email
        assert user_response["username"] == variables["username"] == user.username
        assert user_response["roleId"] == variables["roleId"] == user.role_id
        assert user_response["profilePicture"]["id"] == variables["profilePictureId"] == user.related_media[0].id
        assert user_response["active"] == variables["active"] == user.active

    @pytest.mark.parametrize("username", [" " * 4, "ab"])
    def test_create_user_with_not_enough_characters(self, client, username):
        self.assert_response_error(
            client=client,
            variables=self._get_variables(username=username),
            query=self.query,
            error_message="Username's length must be a minimum of 3 characters."
        )

    @pytest.mark.parametrize("email", [
        "invalid_email@com", "john.doe@example", "no_at_symbol.com",
        "missing_domain@.com", "extra@dots..com", "adryell",
        "spaces in@email.com", "double@@symbol.com", "invalid#character.com"
    ])
    def test_create_user_with_invalid_email(self, client, email):
        self.assert_response_error(
            client=client,
            error_message="Invalid Email.",
            query=self.query,
            variables=self._get_variables(email=email)
        )

    @pytest.mark.parametrize("password, reason", [
        (" " * 4, INVALID_LENGTH),
        ("1234", INVALID_LENGTH),
        ("aaaaaaaa", MISSING_CASE_LETTER),
        ("AAAAAAAA", MISSING_CASE_LETTER),
        ("AaAaAaAa", MISSING_NUMBERS),
        ("AaAa12aA", MISSING_SPECIAL_CHARACTERS)
    ])
    def test_create_user_with_invalid_password(self, client, password, reason):
        self.assert_response_error(
            client=client,
            variables=self._get_variables(password=password),
            query=self.query,
            error_message=reason
        )

    def test_create_user_with_email_already_in_use(self, client, common_user):
        self.assert_response_error(
            client=client,
            query=self.query,
            variables=self._get_variables(email=common_user.email),
            error_message="Email already in use."
        )

    def test_create_user_with_username_already_in_use(self, client, common_user):
        self.assert_response_error(
            client=client,
            query=self.query,
            variables=self._get_variables(username=common_user.username),
            error_message="Username already in use."
        )

    def test_create_user_with_invalid_role(self, client):
        self.assert_response_error(
            client=client,
            variables=self._get_variables(role_id=1000),
            error_message="Role not found.",
            query=self.query
        )

    def test_create_user_with_non_existent_media_item(self, client):
        self.assert_response_error(
            error_message="Media Item not found.",
            variables=self._get_variables(profile_picture_id=1000),
            client=client,
            query=self.query
        )

    def test_create_user_with_non_profile_picture_media_item(self, client, anime_picture_media):
        self.assert_response_error(
            variables=self._get_variables(),
            query=self.query,
            client=client,
            error_message="Media is not in valid type."
        )
