from re import compile


def is_valid_time(time: str) -> dict:
    _time_pattern = compile(r"^[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$")
    if not _time_pattern.match(time):
        return {"valid": False, "message": "The time string is not in the correct format"}

    _hour, _minute, _second = time.split(":")
    if not (0 <= int(_hour) < 24):
        return {"valid": False, "message": "The hour is not within the valid range (0-23)"}
    if not (0 <= int(_minute) < 60):
        return {"valid": False, "message": "The minute is not within the valid range (0-59)"}
    if not (0 <= int(_second) < 60):
        return {"valid": False, "message": "The second is not within the valid range (0-59)"}

    return {"valid": True, "message": "The time is valid"}
