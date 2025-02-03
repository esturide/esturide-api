from app.core.exception import InvalidDataException


def get_username(value: int | str) -> int:
    if isinstance(value, int):
        return value

    try:
        return int(value)
    except (TypeError, ValueError):
        raise InvalidDataException(
            detail="User code is invalid."
        )
