from uuid import uuid4
from data.regions import regions
from database.MySQL.execute_command import execute_command
from entities.driver import Driver


def add_driver() -> dict:
    _instance = Driver()

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

    while _instance.date_of_hire == "null":
        _instance.date_of_hire = input("Please enter your date of hire (required)\n>>> ")

    while _instance.education == "null":
        _instance.education = input("Please enter your education (required)\n>>> ")

    while _instance.license == "null":
        _instance.license = input("Please enter your license (required)\n>>> ")

    _result = execute_command(f"INSERT INTO person VALUES(%s, %s, %s, %s, %s, NULL, %s, %s, %s, NULL)",
                              [_instance.id, _instance.first_name, _instance.last_name, _instance.region,
                               _instance.phone_number, _instance.date_of_birth, _instance.gender, _instance.address])

    if not _result["execute"]:
        return {"add": False, "message": _result["message"]}

    _result = execute_command(f"INSERT INTO employee VALUES(%s, %s, %s, NULL, NULL)",
                              [_instance.id, _instance.date_of_birth, _instance.education])

    if not _result["execute"]:
        return {"add": False, "message": _result["message"]}

    _result = execute_command(f"INSERT INTO driver VALUES(%s, %s, True)",
                              [_instance.id, _instance.license])

    if not _result["execute"]:
        return {"add": False, "message": _result["message"]}

    return {"add": True, "data": _instance.id}
