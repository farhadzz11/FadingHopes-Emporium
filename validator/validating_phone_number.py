from data.regions import regions


def is_valid_phone_number(phone_number: str, region: str) -> dict:
    if not phone_number.isnumeric():
        return {"valid": False,
                "message": "The phone number you entered contains invalid characters\nphone numbers must be numeric"}

    _min_length = 0
    _max_length = 0

    match region:
        case "AU":
            _min_length = 9
            _max_length = 10
        case "CN":
            _min_length = 10
            _max_length = 11
        case "DE":
            _min_length = _max_length = 11
        case "JP":
            _min_length = 9
            _max_length = 10
        case "KR":
            _min_length = 6
            _max_length = 10
        case _:
            if region in ("CA", "GB", "IR", "IN", "IT", "MX", "US"):
                _min_length = _max_length = 10
            elif region in ("ES", "FR"):
                _min_length = _max_length = 9
            else:
                return {"valid": False, "message": "\n\033[31mThe region code is invalid\nThe region code must be a "
                                                   "two-letter code that identifies the country\nThe following are "
                                                   "the countries supported in this program, along with their "
                                                   f"country codes\n{regions.keys()}\033[0m\n"}

    if not (_min_length <= len(phone_number) <= _max_length):
        return {"valid": False, "message": "The phone number you entered is too long or too short\nThe maximum "
                                           f"length is {_max_length} characters and the minimum length is "
                                           f"{_min_length} characters"}

    return {"valid": True, "message": "The phone number isvalid"}
