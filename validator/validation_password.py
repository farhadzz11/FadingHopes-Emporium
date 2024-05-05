from string import punctuation


def is_valid_password(password: str) -> dict:
    if not (11 < len(password) < 121):
        return {"valid": False,
                "message": "The password you entered is too long or too short\nThe maximum length is 120 "
                           "characters and the minimum length is 12 characters"}

    _character_category_flags = {
        "lowercase": False,
        "uppercase": False,
        "digit": False,
        "punctuation": False
    }

    for charactor in password:
        if all(_character_category_flags.values()):
            break

        if charactor.islower():
            _character_category_flags["lowercase"] = True

        elif charactor.isupper():
            _character_category_flags["uppercase"] = True

        elif charactor.isdigit():
            _character_category_flags["digit"] = True

        elif charactor in punctuation:
            _character_category_flags["punctuation"] = True

    if not all(_character_category_flags.values()):
        return {"valid": False, "message": "Password must contain at least one character from each of the following "
                                           "categories:\nLowercase letters: a, b, c, d, ...\nUppercase letters: A, B, "
                                           "C, D, ...\nDigits: 0, 1, 2, 3, ...\nPunctuation: !, @, #, $, ..."}

    return {"valid": True, "message": "The password is valid"}
