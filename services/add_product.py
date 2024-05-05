from uuid import uuid4
from data.regions import regions
from database.MySQL.execute_command import execute_command
from entities.product import Product


def add_product() -> dict:
    _instance = Product()

    _instance.id = str(uuid4())

    while _instance.salesperson_id == "null":
        _instance.salesperson_id = input("Please enter the ID of the seller from "
                                         "whom you purchased this product (required)\n>>> ")

    while _instance.name == "null":
        _instance.name = input("Please enter your product name (required)\n>>> ")

    while _instance.group.lower() == "null":
        _instance.group = input(f"Please enter your product group (required)\n>>> ")

    while _instance.price.lower() == "null":
        _instance.price = input("Please enter your product price (required)\n>>> ")

    while _instance.inventory == 0:
        try:
            _instance.inventory = int(input("Please enter your product inventory (required)\n>>> "))
        except Exception as e:
            print(f"\n\033[31m{e}\033[0m\n")
            continue

    while _instance.manufacture_date == "null":
        _instance.manufacture_date = input("Please enter your product manufacture date (required)\n>>> ")

    while _instance.description == "null":
        _instance.description = input("Please enter your product description (optional)\n>>> ")

    _result = execute_command(f"INSERT INTO product VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                              [_instance.id, _instance.salesperson_id, _instance.name, _instance.group,
                               _instance.price, _instance.inventory, _instance.manufacture_date, _instance.description])

    if not _result["execute"]:
        return {"add": False, "message": _result["message"]}

    return {"add": True, "data": _instance.id}
