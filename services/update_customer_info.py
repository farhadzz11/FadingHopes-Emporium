from database.MySQL.execute_command import execute_command
from services.show_customer_info import show_customer_info
from services.parse_phone_region import parse_phone_region
from validator.validation_name import is_valid_name
from validator.validating_phone_number import is_valid_phone_number
from validator.validation_date import is_valid_date
from validator.validation_email import is_valid_email
from validator.validation_address import is_valid_address
from validator.validation_username import is_valid_username
from validator.validation_password import is_valid_password


def update_customer_info(customer_id: str) -> dict:
    _result = ""
    _result = execute_command("SELECT freight_status FROM freight WHERE factor_id = "
                              "(SELECT factor_id FROM factor WHERE customer_id = %s "
                              "ORDER BY factor_date DESC, factor_time DESC LIMIT 1)", (customer_id,))

    if not _result["execute"]:
        return {"update": False, "message": _result["message"]}

    if len(_result["data"]) != 0:
        if _result["data"][0][0] != "shipped":
            return {"update": False,
                    "message": "You have an order in progress. You cannot edit your information at this time"}

    while True:
        _result = show_customer_info(customer_id)

        if not _result["show"]:
            return {"update": False, "message": _result["message"]}

        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                             "▐   Edit first name      ->     ENTER 1    ▌\n"
                             "▐   Edit last name       ->     ENTER 2    ▌\n"
                             "▐   Edit phone number    ->     ENTER 3    ▌\n"
                             "▐   Edit email           ->     ENTER 4    ▌\n"
                             "▐   Edit date of birth   ->     ENTER 5    ▌\n"
                             "▐   Edit address         ->     ENTER 6    ▌\n"
                             "▐   Edit username        ->     ENTER 7    ▌\n"
                             "▐   Edit password        ->     ENTER 8    ▌\n"
                             "▐   Go back              ->     ENTER 9    ▌\n"
                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")
        _old_info = ""
        _new_info = ""

        match _user_choice:
            case "1":
                _result = execute_command("SELECT person_firstName FROM person WHERE person_id = %s",
                                          (customer_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new first name (old -> {_old_info})\n"
                                      "If you want it to remain the previous value, enter 0\n>>> ")
                    if _new_info.lower() == "null":
                        print("\n\033[31mYou cannot use the phrase \"null\"\033[0m\n")
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == "0":
                        break

                    _new_info = _new_info.strip()
                    _result = is_valid_name(_new_info)

                    if not _result["valid"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE person SET person_firstName = %s WHERE person_id = %s",
                                              [_new_info, customer_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break

            case "2":
                _result = execute_command("SELECT person_lastName FROM person WHERE person_id = %s",
                                          (customer_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new last name (old -> {_old_info})\n"
                                      "If you want it to remain the previous value, enter 0\n>>> ")
                    if _new_info.lower() == "null":
                        print("\n\033[31mYou cannot use the phrase \"null\"\033[0m\n")
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == "0":
                        break

                    _new_info = _new_info.strip()
                    _result = is_valid_name(_new_info)

                    if not _result["valid"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE person SET person_lastName = %s WHERE person_id = %s",
                                              [_new_info, customer_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break

            case "3":
                _result = execute_command("SELECT person_phoneNumber FROM person WHERE person_id = %s",
                                          (customer_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new phone number (old -> {_old_info})\n"
                                      "If you want it to remain the previous value, enter 0\n>>> ")
                    if _new_info.lower() == "null":
                        print("\n\033[0mYou cannot use the phrase \"null\"\033[0m\n")
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == "0":
                        break

                    _result = execute_command("SELECT person_region FROM person WHERE person_id = %s",
                                              (customer_id,))

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}

                    _new_info = _new_info.strip()

                    if _result["data"][0][0] == "null":
                        print("\n\033[0mThe region field cannot be empty\nPlease enter it first\033[0m\n")
                        continue

                    _region = _result["data"][0][0]

                    if _new_info.startswith("0"):
                        _new_info = _new_info[1:]

                    _result = is_valid_phone_number(_new_info, _result["data"][0][0])

                    if not _result["valid"]:
                        print(f"\n\033[0m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE person "
                                              f"SET person_phoneNumber = "
                                              f"'+{parse_phone_region(_new_info, _region)}{_new_info}' "
                                              f"WHERE person_id = %s",
                                              (customer_id,))

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "4":
                _result = execute_command("SELECT person_email FROM person WHERE person_id = %s",
                                          (customer_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new email (old -> {_old_info})\n"
                                      "If you want it to remain the previous value, enter 0\n>>> ")
                    if _new_info.lower() == "null":
                        print("\n\033[31mYou cannot use the phrase \"null\"\033[0m\n")
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == "0":
                        break

                    _new_info = _new_info.strip()
                    _result = is_valid_email(_new_info)

                    if not _result["valid"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE person SET person_email = %s WHERE person_id = %s",
                                              [_new_info, customer_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "5":
                _result = execute_command("SELECT person_dateOfBirth FROM person WHERE person_id = %s",
                                          (customer_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new date of birth (old -> {_old_info})\n"
                                      "If you want it to remain the previous value, enter 0\n>>> ")
                    if _new_info.lower() == "null":
                        print("\n\033[31mYou cannot use the phrase \"null\"\033[0m\n")
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == "0":
                        break

                    _new_info = _new_info.strip()
                    _result = is_valid_date(_new_info)

                    if not _result["valid"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE person SET person_dateOfBirth = %s WHERE person_id = %s",
                                              [_new_info, customer_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "6":
                _result = execute_command("SELECT person_address FROM person WHERE person_id = %s",
                                          (customer_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new address (old -> {_old_info})\n"
                                      "If you want it to remain the previous value, enter 0\n>>> ")
                    if _new_info.lower() == "null":
                        print("\n\033[31mYou cannot use the phrase \"null\"\033[0m\n")
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == "0":
                        break

                    _new_info = _new_info.strip()
                    _result = is_valid_address(_new_info)

                    if not _result["valid"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE person SET person_address = %s WHERE person_id = %s",
                                              [_new_info, customer_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "7":
                _result = execute_command("SELECT customer_username FROM customer WHERE person_id = %s",
                                          (customer_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new username (old -> {_old_info})\n"
                                      "If you want it to remain the previous value, enter 0\n>>> ")
                    if _new_info.lower() == "null":
                        print("\n\033[31mYou cannot use the phrase \"null\"\033[0m\n")
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == "0":
                        break

                    _new_info = _new_info.strip()
                    _result = is_valid_username(_new_info)

                    if not _result["valid"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("SELECT customer_username FROM customer WHERE customer_username = %s",
                                              (_new_info,))

                    if not _result["execute"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    if len(_result["data"]) != 0:
                        print(f"\n\033[31mThe username already exists\nPlease enter another username\033[0m\n")
                        continue

                    _result = execute_command("UPDATE customer SET customer_username = %s WHERE person_id = %s",
                                              [_new_info, customer_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "8":
                _result = execute_command("SELECT customer_password FROM customer WHERE person_id = %s",
                                          (customer_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new password (old -> {_old_info})\n"
                                      "If you want it to remain the previous value, enter 0\n>>> ")
                    if _new_info.lower() == "null":
                        print("\n\033[31mYou cannot use the phrase \"null\"\033[0m\n")
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == "0":
                        break

                    _result = is_valid_password(_new_info)

                    if not _result["valid"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE customer SET customer_password = %s WHERE person_id = %s",
                                              [_new_info, customer_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "9":
                break
            case _:
                print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                continue
        print(f"\n{_old_info} successfully changed to {_new_info}\n")

    return {"update": True, "message": "information successfully updated"}
