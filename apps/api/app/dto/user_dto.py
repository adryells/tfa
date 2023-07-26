import re

from pydantic import BaseModel, validate_email, validator

from app.dto import BaseValidator


def validate_username(username: str):
    if username:
        username = username.strip()

        if len(username) < 3:
            raise Exception("Username's length must be a minimum of 3 characters.")

    return username


def validate_user_email(email: str):
    if email:
        email = email.strip().lower()

        try:
            validate_email(email)

        except Exception as _:
            raise Exception("Invalid Email.")

    return email


def validate_password(password: str):
    if password:
        if not password.strip() or len(password) < 8:
            raise Exception("Password must have at least 8 characters.")

        if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            raise Exception("Password must contain both uppercase and lowercase letters.")

        if not any(char.isdigit() for char in password):
            raise Exception("Password must contain numbers.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise Exception("Password must contain special characters.")

    return password


class InputCreateUserDataValidator(BaseValidator):
    username: str

    email: str

    password: str

    role_id: int

    profile_picture_id: int

    active: bool

    @validator("username")
    def validate_username(cls, value: str): # noqa
        return validate_username(value)

    @validator("email")
    def validate_email(cls, value: str): # noqa
        return validate_user_email(value)

    @validator("password")
    def validate_password(cls, value: str): # noqa
        return validate_password(value)

    @validator("role_id", "profile_picture_id")
    def validate_value_id(cls, value: int): # noqa
        cls.validate_id(value)

        return value


class InputPasswordDataValidator(BaseModel):
    current_password: str

    new_password: str

    @validator("current_password", "new_password")
    def validate_new_password(cls, value: str): # noqa
        return validate_password(value)


class InputUpdateUserDataValidator(InputCreateUserDataValidator):
    user_id: int

    username: str | None

    email: str | None

    input_password: InputPasswordDataValidator | None

    password: None = None

    role_id: int | None

    profile_picture_id: int | None

    active: bool | None


class InputSignupDataValidator(BaseModel):
    email: str
    username: str
    password: str

    @validator("username")
    def validate_username(cls, value: str): # noqa
        return validate_username(value)

    @validator("email")
    def validate_email(cls, value: str): # noqa
        return validate_user_email(value)

    @validator("password")
    def validate_password(cls, value: str): # noqa
        return validate_password(value)
