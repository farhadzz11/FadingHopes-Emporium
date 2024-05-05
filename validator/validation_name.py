from data.offensive_words import offensive_words


def is_valid_name(name: str) -> dict:
    if not (1 < len(name) < 31):
        return {"valid": False, "message": "The name you entered is too long or too short\nThe maximum length is 30 "
                                           "characters and the minimum length is 2 characters"}

    if not name.isalpha():
        return {"valid": False, "message": "The name you entered contains invalid characters. Names must be "
                                           "alpha and cannot contain spaces\nPlease enter a name that is "
                                           "alpha and does not contain spaces"}

    if name.lower() in offensive_words:
        return {"valid": False, "message": "Your name contains language that is considered offensive to some "
                                           "people\nWe want to create a safe shopping environment for everyone\n"
                                           "Offensive language can make people feel uncomfortable or unsafe"}

    return {"valid": True, "message": "The name is valid"}
