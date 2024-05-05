def is_valid_quantity(quantity: int) -> dict:
    if not isinstance(quantity, int):
        return {"valid": False, "message": "quantity must be an integer"}

    if not (0 < quantity < 101):
        return {"valid": False, "message": "Quantity must be between 1 and 100\nThis is to ensure a positive and "
                                           "manageable quantity"}

    return {"valid": True, "message": "The quantity is valid"}
