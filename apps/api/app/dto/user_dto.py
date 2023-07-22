from pydantic import BaseModel, validate_email, validator


class InputCreateUserDataValidator(BaseModel):
    username: str

    email: str

    password: str

    role_id: int

    profile_picture_id: int

    active: bool

    @validator("username")
    def validate_username(cls, value: str): # noqa
        if not value.strip():
            raise Exception("Username can't be blank.")

        return value.lower().capitalize()

    @validator("email")
    def validate_email(cls, value: str): # noqa
        value = value.strip().lower()

        if not validate_email(value):
            raise Exception("Invalid Email.")

        return value

    @validator("password")
    def validate_password(cls, value: str): # noqa
        if not value.strip() or len(value) < 8:
            raise Exception("Invalid Password.")

        return value

    @validator("role_id", "profile_picture_id")
    def validate_id(cls, value: int): # noqa
        if value <= 0:
            raise Exception("Invalid id.")

        return value


class InputPasswordDataValidator(BaseModel):
    current_password: str

    new_password: str

    @validator("current_password", "new_password")
    def validate_new_password(cls, value: str): # noqa
        if not value.strip() or len(value) < 8:
            raise Exception("Invalid Password.")

        return value


class InputUpdateUserDataValidator(InputCreateUserDataValidator):
    user_id: int

    username: str | None

    email: str | None

    input_password: InputPasswordDataValidator | None

    role_id: int | None

    profile_picture_id: int | None

    active: bool | None

    @validator("password")
    def validate_password(cls, value: str): # noqa
        return value


# TODO: Dá pra refatorar e amenizar a repetição de código
class InputSignupDataValidator(BaseModel):
    email: str
    username: str
    password: str

    @validator("username")
    def validate_username(cls, value: str): # noqa
        if not value.strip():
            raise Exception("Username can't be blank.")

        return value.lower().capitalize()

    @validator("email")
    def validate_email(cls, value: str): # noqa
        value = value.strip().lower()

        if not validate_email(value):
            raise Exception("Invalid Email.")

        return value

    @validator("password")
    def validate_password(cls, value: str): # noqa
        if not value.strip() or len(value) < 8:
            raise Exception("Invalid Password.")

        return value
