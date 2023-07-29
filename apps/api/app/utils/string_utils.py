# FAIL PASSWORD REASONS
INVALID_LENGTH = "Password must have at least 8 characters."
MISSING_CASE_LETTER = "Password must contain both uppercase and lowercase letters."
MISSING_NUMBERS = "Password must contain numbers."
MISSING_SPECIAL_CHARACTERS = "Password must contain special characters."


def to_lower_camel_case(snake_str: str) -> str:
    camel_string = snake_str.title().replace("_", "")

    return camel_string[0].lower() + camel_string[1:]
