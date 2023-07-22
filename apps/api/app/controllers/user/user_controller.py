from app.controllers import BaseController
from app.data.media_type import profile_picture
from app.data.role import admin, common
from app.dto.user_dto import InputCreateUserDataValidator, InputUpdateUserDataValidator, InputSignupDataValidator
from app.models.user.basic import User
from app.queries.media_item.media_item_queries import MediaItemQueries
from app.queries.role.role_queries import RoleQueries
from app.queries.user.user_queries import UserQueries


class UserController(BaseController):
    def get_user_by_id(self, user_id: int) -> User:
        user = UserQueries(self.session).get_user_by_id(user_id=user_id)

        if not user:
            raise Exception("User not found.")

        return user

    def check_media_exists_and_is_type(self, type_name: str, media_id: int):
        media = MediaItemQueries(self.session).get_media_item_by_id(media_id)

        if not media:
            raise Exception("Media Item not found.")

        media_is_type = media.media_type.name == type_name

        if not media_is_type:
            raise Exception("Media is not in valid type.")

    def create_user(self, data: InputCreateUserDataValidator) -> User:
        role = RoleQueries(self.session).get_role_by_id(data.role_id)

        if not role:
            raise Exception("Role not found.")

        self.check_media_exists_and_is_type(type_name=profile_picture.name, media_id=data.profile_picture_id)

        new_user = User(
            username=data.username, # noqa
            email=data.email, # noqa
            active=data.active, # noqa
            role=role # noqa
        )

        new_profile_picture = MediaItemQueries(self.session).get_media_item_by_id(data.profile_picture_id)

        new_user.related_media.append(new_profile_picture)
        new_user.set_password(data.password)

        self.session.add(new_user)
        self.session.commit()

        return new_user

    # TODO: Dá pra dar uma refatoradinha pra n precisar da gambi e continuar reduzido o código
    def signup(self, data: InputSignupDataValidator) -> User:
        role = RoleQueries(self.session).get_role_by_name(common.name)

        user = User(
            role=role, # noqa
            username="gambi", # noqa
            email="gambi@tfa.tfa" # noqa
        )

        user.set_password(data.password)
        self.update_user_email(user, data.email)
        self.update_user_username(user, data.username)

        self.session.add(user)
        self.session.commit()

        return user

    def update_user(self, data: InputUpdateUserDataValidator, updater_user_id: int) -> User:
        updating_user = self.get_user_by_id(user_id=data.user_id)

        is_self_update = updater_user_id == data.user_id
        updater_user_is_admin = UserQueries(self.session).user_has_role(role_name=admin.name, user_id=updater_user_id)

        if not is_self_update and not updater_user_is_admin:
            raise Exception("You can't update another user.")

        user_handler = {
            "active": lambda: self.update_attribute_object(updating_user, "active", data.active),
            "username": lambda: self.update_user_username(updating_user, data.username),
            "email": lambda: self.update_user_email(updating_user, data.email),
            "password": lambda: self.update_user_password(
                updating_user=updating_user,
                current_password=data.input_password.current_password,
                new_password=data.input_password.new_password
            ),
            "role_id": lambda: self.update_user_role(updating_user, updater_user_is_admin, data.role_id),
            "profile_picture_id": lambda: self.update_profile_picture(updating_user, data.profile_picture_id)
        }

        for key, value in data.__dict__.items():
            if key in user_handler and value is not None:
                user_handler[key]()

        self.session.commit()

        return updating_user

    def update_user_username(self, updating_user: User, username: str):
        username_in_use = UserQueries(self.session).check_user_exists_by_username(username=username)

        if username_in_use:
            raise Exception("Username already in use.")

        updating_user.username = username

    def update_user_email(self, updating_user: User, email: str):
        email_in_use = UserQueries(self.session).check_user_exists_by_email(email=email)

        if email_in_use:
            raise Exception("Email already in use.")

        updating_user.email = email

    def update_user_password(self, updating_user: User, current_password: str, new_password: str): # noqa
        password_match = updating_user.password_match(current_password)

        if not password_match:
            raise Exception("Wrong current password.")

        updating_user.set_password(new_password)

    def update_user_role(self, updating_user: User, updater_user_is_admin: bool, role_id: int):
        if not updater_user_is_admin:
            raise Exception("Only an admin can update roles from another user.")

        role = RoleQueries(self.session).get_role_by_id(role_id=role_id)

        updating_user.role = role

    def update_profile_picture(self, updating_user: User, profile_picture_id: int):
        media_item_queries = MediaItemQueries(self.session)

        self.check_media_exists_and_is_type(type_name=profile_picture.name, media_id=profile_picture_id)

        for media in updating_user.related_media:
            if media.media_type.name == profile_picture.name:
                updating_user.related_media.remove(media)
                break

        new_profile_picture = media_item_queries.get_media_item_by_id(profile_picture_id)

        updating_user.related_media.append(new_profile_picture)

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)

        user.delete()

        self.session.commit()

    def get_users(self, page: int, per_page: int, search: str):
        self._validate_filters(page=page, per_page=per_page)

        users = UserQueries(self.session).get_users(page=page, per_page=per_page, search=search)

        return users

    def _validate_filters(self, page: int, per_page: int):
        if (page is not None and per_page is not None) and (page < 1 or per_page < 1):
            raise Exception("Invalid Pagination.")

    def get_users_count(self, search: str):
        count = UserQueries(self.session).get_users_count(search=search)

        return count
    