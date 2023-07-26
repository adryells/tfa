from tests import BaseTest


class TestUpdateUser(BaseTest):
    query = """
    mutation updateUser(
      $userId: Int!
    ){
      UpdateUser(
        inputUpdateUserData: {
          userId: $userid,
          username: $username,
          email: $email,
          inputPassword: {currentPassword: $current_password, newPassword: $new_password},
          roleId: $roleid,
          profilePictureId: $profilepictureid,
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
