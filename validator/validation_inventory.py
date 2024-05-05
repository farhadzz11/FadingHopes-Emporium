def is_valid_inventory(inventory: int) -> dict:
    if not isinstance(inventory, int):
        return {"valid": False, "message": "Inventory must be an integer"}

    if not (0 <= inventory < 32768):
        return {"valid": False, "message": "Inventory must be between 0 and 32767\nThis is to ensure a positive and "
                                           "manageable inventory"}

    return {"valid": True, "message": "The inventory is valid"}
