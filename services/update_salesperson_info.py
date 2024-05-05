from data.academic_degrees import academic_degrees
from database.MySQL.execute_command import execute_command
from services.show_salespersons import show_a_salesperson
from services.parse_phone_region import parse_phone_region
from validator.validation_name import is_valid_name
from validator.validating_phone_number import is_valid_phone_number
from validator.validation_date import is_valid_date
from validator.validation_email import is_valid_email
from validator.validation_address import is_valid_address
from validator.validation_work_experience import is_valid_work_experience


def update_salesperson_info(salesperson_id: str) -> dict:
    while True:
        _result = show_a_salesperson(salesperson_id)

        if not _result["show"]:
            return {"update": False, "message": _result["message"]}

        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                             "▐   Edit first name                   ->     ENTER 1     ▌\n"
                             "▐   Edit last name                    ->     ENTER 2     ▌\n"
                             "▐   Edit phone number                 ->     ENTER 3     ▌\n"
                             "▐   Edit email                        ->     ENTER 4     ▌\n"
                             "▐   Edit date of birth                ->     ENTER 5     ▌\n"
                             "▐   Edit address                      ->     ENTER 6     ▌\n"
                             "▐   Edit date of hire                 ->     ENTER 7     ▌\n"
                             "▐   Edit education                    ->     ENTER 8     ▌\n"
                             "▐   Edit work experience              ->     ENTER 9     ▌\n"
                             "▐   Edit legal information            ->     ENTER 10    ▌\n"
                             "▐   Go back                           ->     ENTER 11    ▌\n"
                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")
        _old_info = ""
        _new_info = ""

        match _user_choice:
            case "1":
                _result = execute_command("SELECT person_firstName FROM person WHERE person_id = %s",
                                          (salesperson_id,))

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
                                              [_new_info, salesperson_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break

            case "2":
                _result = execute_command("SELECT person_lastName FROM person WHERE person_id = %s",
                                          (salesperson_id,))

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
                                              [_new_info, salesperson_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break

            case "3":
                _result = execute_command("SELECT person_phoneNumber FROM person WHERE person_id = %s",
                                          (salesperson_id,))

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
                                              (salesperson_id,))

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
                                              (salesperson_id,))

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "4":
                _result = execute_command("SELECT person_email FROM person WHERE person_id = %s",
                                          (salesperson_id,))

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
                                              [_new_info, salesperson_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "5":
                _result = execute_command("SELECT person_dateOfBirth FROM person WHERE person_id = %s",
                                          (salesperson_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new date (old -> {_old_info})\n"
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
                                              [_new_info, salesperson_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "6":
                _result = execute_command("SELECT person_address FROM person WHERE person_id = %s",
                                          (salesperson_id,))

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
                                              [_new_info, salesperson_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "8":
                _result = execute_command("SELECT employee_education FROM employee WHERE person_id = %s",
                                          (salesperson_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new education (old -> {_old_info})\n"
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
                    if _new_info not in academic_degrees:
                        print(
                            "\n\033[31mThe education you entered is invalid. "
                            "Please select an education from the following "
                            f"list\n{academic_degrees}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE employee SET employee_education = %s "
                                              "WHERE person_id = %s",
                                              [_new_info, salesperson_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "9":
                _result = execute_command("SELECT employee_workExperience FROM employee WHERE person_id = %s",
                                          (salesperson_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}
                _old_info = _result["data"][0][0]
                _new_info = []

                while True:
                    try:
                        _count = int(input("How many work experiences?\n>>> "))
                        break
                    except Exception as e:
                        print(e)

                _index = 0
                while _index < _count:
                    _temp = [input(f"Please enter your new company name "
                                   f"for work experience[{_index + 1}]\n>>> "),
                             input(f"Please enter your new job title "
                                   f"for work experience[{_index + 1}]\n>>> "),
                             input(f"Please enter your new start date "
                                   f"for work experience[{_index + 1}]\n>>> "), input(f"Please enter your new end date "
                                                                                      f"for work experience"
                                                                                      f"[{_index + 1}]"
                                                                                      f"\n>>> "),
                             input(f"Please enter your new description "
                                   f"for work experience[{_index + 1}]\n>>> ")]

                    _result = is_valid_work_experience(_temp)
                    if _result["valid"]:
                        print("----")
                        _new_info.append(_temp)
                        _index += 1
                        continue
                    else:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")

                _result = execute_command("UPDATE employee SET employee_workExperience = %s "
                                          "WHERE person_id = %s", [str(_new_info), salesperson_id])

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}
            case "10":
                _result = execute_command("SELECT employee_legalInformation FROM employee WHERE person_id = %s",
                                          (salesperson_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]
                _new_info = ""

                while True:
                    _new_info = input(f"Please enter your new education (old -> {_old_info})\n"
                                      "If you want it to remain the previous value, enter 0\n>>> ")
                    if _new_info.lower() == "null":
                        print("\n\033[31mYou cannot use the phrase \"null\"\033[0m\n")
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == "0":
                        break

                    if not (0 <= len(_new_info) <= 255):
                        print("\n\033[31mThe legal information must be between 0 and 255 characters long\033[0m\n")
                        continue
                    else:
                        break

                _result = execute_command("UPDATE employee SET employee_legalInformation = %s "
                                          "WHERE person_id = %s",
                                          [_new_info, salesperson_id])

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}
            case "11":
                break
            case _:
                if _user_choice in ["5", "7"]:
                    _result = execute_command("SELECT person_dateOfBirth FROM person WHERE person_id = %s",
                                              (salesperson_id,))

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}

                    _old_info = _result["data"][0][0]
                    _new_info = ""

                    while True:
                        _new_info = input(f"Please enter your new date (old -> {_old_info})\n"
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
                                                  [_new_info, salesperson_id])

                        if not _result["execute"]:
                            return {"update": False, "message": _result["message"]}
                        break
                else:
                    print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                    continue
        print(f"\n{_old_info} successfully changed to {_new_info}\n")

    return {"update": True, "message": "information successfully updated"}
