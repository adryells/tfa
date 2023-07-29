from datetime import datetime

from tests import BaseTest
from tests.utils import format_date_graphql


class TestUpdateUser(BaseTest):
    query = """
        mutation updateUser(
          $user_id: Int!,
          $username: String,
          $email: String,
          $current_password: String!,
          $new_password: String!,
          $role_id: Int,
          $profile_picture_id: Int,
          $active: Boolean
        ){
          UpdateUser(
            inputUpdateUserData: {
              userId: $user_id,
              username: $username,
              email: $email,
              inputPassword: {currentPassword: $current_password, newPassword: $new_password},
              roleId: $role_id,
              profilePictureId: $profile_picture_id,
              active: $active
            }
          ){
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
            role_id: int = 1,
            active: bool = False,
            current_password: str = "12345678",
            new_password: str = "@AaaAaA12",
            email: str = "aefghyz@tfa.tfa",
            username: str = "aefghyz",
            user_id: int = 1
    ) -> dict:
        return {
            "active": active,
            "profile_picture_id": profile_picture_id,
            "role_id": role_id,
            "current_password": current_password,
            "new_password": new_password,
            "email": email,
            "username": username,
            "user_id": user_id
        }

    def test_request_without_token(self, client):
        self.assert_with_invalid_token(client=client, query=self.query, variables=self._get_variables())

    def test_request_with_invalid_structure_token(self, client):
        self.assert_with_invalid_token(
            client=client,
            query=self.query,
            token="hahaha 123",
            variables=self._get_variables()
        )

    def test_request_with_invalid_token(self, client):
        self.assert_with_invalid_token(
            client=client,
            query=self.query,
            token="TfaApiTok = isso ai",
            variables=self._get_variables(),
            error_message="Token doesn't match any user."
        )

    def test_request_without_permission(self, client, common_user_auth_token):
        self.assert_with_invalid_token(
            client=client,
            query=self.query,
            token=common_user_auth_token.token,
            error_message="You don't have permission for this service.",
            variables=self._get_variables()
        )

    def test_update_user_success(self, client, common_user_auth_token, profile_picture_media):
        variables = self._get_variables(
            user_id=common_user_auth_token.user.id,
            active=not common_user_auth_token.active,
            profile_picture_id=profile_picture_media.id,
            role_id=2
        )

        response = self.request_api(
            client=client,
            variables=variables,
            query=self.query,
            token=common_user_auth_token.token
        )

        assert response["data"]["UpdateUser"]["user"]

        user_response = response["data"]["UpdateUser"]["user"]

        assert user_response["id"] == common_user_auth_token.user.id
        assert user_response["username"] == common_user_auth_token.user.username == variables["username"]
        assert user_response["createdAt"] == format_date_graphql(common_user_auth_token.user.created_at)
        assert user_response["updatedAt"] == format_date_graphql(common_user_auth_token.user.updated_at)
        assert user_response["email"] == common_user_auth_token.user.email == variables["email"]
        assert user_response["active"] == common_user_auth_token.user.active == variables["active"]
        assert user_response["roleId"] == common_user_auth_token.user.role_id == variables["role_id"]
        assert user_response["profilePicture"]["id"] == profile_picture_media.id == variables["profile_picture_id"]

    def test_update_user_with_invalid_role_id(self, client, common_user_auth_token, profile_picture_media):
        variables = self._get_variables(
            user_id=common_user_auth_token.user.id,
            active=not common_user_auth_token.user.active,
            profile_picture_id=profile_picture_media.id,
            role_id=1000
        )

        self.assert_response_error(
            client=client,
            variables=variables,
            error_message="Role not found.",
            query=self.query,
            token=common_user_auth_token.token
        )

    def test_update_user_with_invalid_user_id(self, client, common_user_auth_token):
        variables = self._get_variables(user_id=1000)

        self.assert_response_error(
            client=client,
            variables=variables,
            error_message="User not found.",
            query=self.query,
            token=common_user_auth_token.token
        )

    def test_update_user_with_invalid_profile_picture_id(self, client, common_user_auth_token):
        variables = self._get_variables(profile_picture_id=1000, user_id=common_user_auth_token.user_id)

        self.assert_response_error(
            client=client,
            query=self.query,
            token=common_user_auth_token.token,
            variables=variables,
            error_message="Media Item not found."
        )

    def test_update_user_with_invalid_media_type(self, client, anime_picture_media, common_user_auth_token):
        variables = self._get_variables(
            profile_picture_id=anime_picture_media.id,
            user_id=common_user_auth_token.user_id
        )

        self.assert_response_error(
            client=client,
            variables=variables,
            error_message="Media is not in valid type.",
            query=self.query,
            token=common_user_auth_token.token
        )

    def test_update_user_with_username_in_use(self, client, common_user_auth_token, profile_picture_media):
        variables = self._get_variables(
            profile_picture_id=profile_picture_media.id,
            user_id=common_user_auth_token.user.id,
            username="tfa_admin"
        )

        self.assert_response_error(
            client=client,
            error_message="Username already in use.",
            variables=variables,
            query=self.query,
            token=common_user_auth_token.token
        )

    def test_update_user_with_email_in_use(self, client, common_user_auth_token, profile_picture_media):
        variables = self._get_variables(
            profile_picture_id=profile_picture_media.id,
            user_id=common_user_auth_token.user.id,
            email="tfa_admin@tfa.tfa"
        )

        self.assert_response_error(
            client=client,
            error_message="Email already in use.",
            variables=variables,
            query=self.query,
            token=common_user_auth_token.token
        )

    def test_update_user_with_wrong_current_password(self, client, common_user_auth_token, profile_picture_media):
        variables = self._get_variables(
            profile_picture_id=profile_picture_media.id,
            user_id=common_user_auth_token.user.id,
            current_password="12345677"
        )

        self.assert_response_error(
            client=client,
            error_message="Wrong current password.",
            variables=variables,
            query=self.query,
            token=common_user_auth_token.token
        )

    def test_update_another_user(self, client, common_user_auth_token, profile_picture_media):
        variables = self._get_variables(profile_picture_id=profile_picture_media.id)

        self.assert_response_error(
            client=client,
            error_message="You can't update another user.",
            variables=variables,
            query=self.query,
            token=common_user_auth_token.token
        )
