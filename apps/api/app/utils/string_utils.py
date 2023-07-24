def to_lower_camel_case(snake_str: str) -> str:
    camel_string = snake_str.title().replace("_", "")

    return camel_string[0].lower() + camel_string[1:]
