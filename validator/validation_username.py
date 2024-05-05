from data.offensive_words import offensive_words


def is_valid_username(username: str) -> dict:
    if not (1 < len(username) < 31):
        return {"valid": False,
                "message": "The username you entered is too long or too short\nThe maximum length is 30 "
                           "characters and the minimum length is 2 characters"}

    if not (all(charactor.isalnum() or charactor == "_" for charactor in username)):
        return {"valid": False, "message": "The username you entered contains invalid characters. Usernames must be "
                                           "alphanumeric and cannot contain spaces\nPlease enter a username that is "
                                           "alphanumeric and does not contain spaces"}

    _username_words = username.split("_")
    for word in _username_words:
        if word.lower() in offensive_words:
            return {"valid": False, "message": "Your username contains language that is considered offensive to some "
                                               "people\nWe want to create a safe shopping environment for everyone\n"
                                               "Offensive language can make people feel uncomfortable or unsafe"}

    return {"valid": True, "message": "The username is valid"}
