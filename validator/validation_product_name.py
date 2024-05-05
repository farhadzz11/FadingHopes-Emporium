from data.offensive_words import offensive_words


def is_valid_product_name(product_name: str) -> dict:
    if not (1 < len(product_name) < 31):
        return {"valid": False,
                "message": "The product name you entered is too long or too short\nThe maximum length is 30 "
                           "characters and the minimum length is 2 characters"}

    if not (all(charactor.isalnum() or charactor == " " for charactor in product_name)):
        return {"valid": False, "message": "The product name you entered contains invalid characters. Product names "
                                           "must be alphanumeric\nPlease enter a product name that is alphanumeric"}

    _username_words = product_name.split(" ")
    for word in _username_words:
        if word.lower() in offensive_words:
            return {"valid": False, "message": "Your product name contains language that is considered offensive to "
                                               "some people\nWe want to create a safe shopping environment for "
                                               "everyone\nOffensive language can make people feel uncomfortable or "
                                               "unsafe"}

    return {"valid": True, "message": "The product name is valid"}
