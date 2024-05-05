from re import compile


def is_valid_uuid4(uuid4: str) -> dict:
    if not isinstance(uuid4, str):
        return {"valid": False, "message": "Invalid ID type. Expected a string"}

    _uuid4_pattern = compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

    if not _uuid4_pattern.match(uuid4):
        return {"valid": False, "message": "The ID format is invalid\nThe ID must be in the format UUID4"}

    return {"valid": True, "message": "The ID is valid"}
