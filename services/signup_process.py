from uuid import uuid4
from data.regions import regions
from database.MySQL.execute_command import execute_command
from entities.customer import Customer


def signup_process() -> dict:
    _instance = Customer()

    _instance.id = str(uuid4())

    while _instance.first_name == "null":
        _instance.first_name = input("Please enter your first name (required)\n>>> ")

    while _instance.last_name == "null":
        _instance.last_name = input("Please enter your last name (required)\n>>> ")

    while _instance.region.lower() == "null":
        _instance.region = input(f"Please enter your region from the given choices (required)\n{regions}\n>>> ")

    while _instance.phone_number.lower() == "null":
        _instance.phone_number = input("Please enter your phone number (required)\n>>> ")

    while _instance.date_of_birth == "null":
        _instance.date_of_birth = input("Please enter your date of birth (required)\n>>> ")

    while _instance.gender == "null":
        _instance.gender = input("Please enter your gender (required)\n>>> ")

    while _instance.address == "null":
        _instance.address = input("Please enter your address (required)\n>>> ")

    while _instance.username == "null":
        _instance.username = input("Please enter your username (required)\n>>> ")

    while _instance.password == "null":
        _instance.password = input("Please enter your password (required)\n>>> ")

    _result = execute_command(f"INSERT INTO person VALUES(%s, %s, %s, %s, %s, NULL, %s, %s, %s, NULL)",
                              [_instance.id, _instance.first_name, _instance.last_name, _instance.region,
                               _instance.phone_number, _instance.date_of_birth, _instance.gender, _instance.address])

    if not _result["execute"]:
        return {"signup": False, "message": _result["message"]}

    _result = execute_command(f"INSERT INTO customer VALUES(%s, %s, %s)",
                              [_instance.id, _instance.username, _instance.password])

    if not _result["execute"]:
        return {"signup": False, "message": _result["message"]}

    return {"signup": True, "data": _instance.id, "access_level": "user"}
