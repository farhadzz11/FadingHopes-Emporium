from data.offensive_words import offensive_words


def is_valid_address(address: str) -> dict:
    if not (27 < len(address) < 256):
        return {"valid": False, "message": "Address length must be between 28 and 255 characters"}

    _required_keywords = ("street", "city", "zipcode")
    for keyword in _required_keywords:
        if keyword not in address.lower():
            return {"valid": False, "message": f"Address must include at least \"{keyword}\""}

    _address_words = address.split(" ")
    for word in _address_words:
        if word.lower() in offensive_words:
            return {"valid": False, "message": "The address contains language that is considered offensive to some "
                                               "people\nWe want to create a safe shopping environment for everyone\n"
                                               "Offensive language can make people feel uncomfortable or unsafe"}

    return {"valid": True, "message": "The address is valid"}
