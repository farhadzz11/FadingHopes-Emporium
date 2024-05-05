from data.product_groups import product_groups
from data.currency_units import currency_units
from database.MySQL.execute_command import execute_command
from services.show_products import show_a_product
from validator.validation_product_name import is_valid_product_name
from validator.validation_price import is_valid_price
from validator.validation_inventory import is_valid_inventory
from validator.validation_date import is_valid_date


def update_product_info(product_id: str) -> dict:
    while True:
        _result = show_a_product(product_id)

        if not _result["show"]:
            return {"update": False, "message": _result["message"]}

        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                             "▐   Edit salesperson id               ->     ENTER 1     ▌\n"
                             "▐   Edit name                         ->     ENTER 2     ▌\n"
                             "▐   Edit group                        ->     ENTER 3     ▌\n"
                             "▐   Edit price                        ->     ENTER 4     ▌\n"
                             "▐   Edit inventory                    ->     ENTER 5     ▌\n"
                             "▐   Edit manufacture date             ->     ENTER 6     ▌\n"
                             "▐   Edit description                  ->     ENTER 7     ▌\n"
                             "▐   Go back                           ->     ENTER 8     ▌\n"
                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")
        _old_info = ""
        _new_info = ""

        match _user_choice:
            case "1":
                _result = execute_command("SELECT employee_id FROM product "
                                          "WHERE product_id = %s", (product_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]

                while True:
                    _new_info = input(f"Please enter your new salesperson id (old -> {_old_info})\n"
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
                    _result = execute_command("SELECT * FROM salesperson WHERE employee_id = %s",
                                              (_new_info,))

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}

                    if len(_result["data"]) == 0:
                        print(f"\n\033[31mThe salesperson ID you entered is not associated "
                              f"with any salespersons in the database\033[0m\n")
                        continue

                    _result = execute_command("UPDATE product SET employee_id = %s WHERE product_id = %s",
                                              [_new_info, product_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break

            case "2":
                _result = execute_command("SELECT product_name FROM product "
                                          "WHERE product_id = %s", (product_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]

                while True:
                    _new_info = input(f"Please enter your new product name (old -> {_old_info})\n"
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
                    _result = is_valid_product_name(_new_info)

                    if not _result["valid"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE product SET product_name = %s WHERE product_id = %s",
                                              [_new_info, product_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "3":
                _result = execute_command("SELECT product_group FROM product "
                                          "WHERE product_id = %s", (product_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]

                while True:
                    _new_info = input(f"Please enter your new product group (old -> {_old_info})\n"
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
                    if _new_info.lower() not in product_groups:
                        print(
                            "\n\033[31mThe product group is invalid\nThe product group must be one of the following: \n"
                            f"{product_groups}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE product SET product_group = %s WHERE product_id = %s",
                                              [_new_info, product_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "4":
                _result = execute_command("SELECT product_price FROM product "
                                          "WHERE product_id = %s", (product_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]

                while True:
                    _new_info = input(f"Please enter your new product price (old -> {_old_info})\n"
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
                    _result = execute_command("SELECT person.person_region FROM person INNER JOIN employee ON "
                                              "person.person_id = employee.person_id "
                                              "INNER JOIN salesperson ON employee.person_id = salesperson.employee_id "
                                              "WHERE person.person_id = "
                                              "(SELECT employee_id FROM product WHERE product_id = %s)",
                                              (product_id,))

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}

                    _region = _result["data"][0][0]

                    _result = is_valid_price(_new_info, _region)

                    if not _result["valid"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE product SET product_price = %s WHERE product_id = %s",
                                              [f"{currency_units[_region]}{_new_info}", product_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "5":
                _result = execute_command("SELECT product_inventory FROM product "
                                          "WHERE product_id = %s", (product_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]

                while True:
                    try:
                        _new_info = int(input(f"Please enter your new product inventory (old -> {_old_info})\n"
                                              "If you want it to remain the previous value, enter -1\n>>> "))
                    except Exception as e:
                        print(e)
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == -1:
                        break

                    _result = is_valid_inventory(_new_info)

                    if not _result["valid"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue

                    _result = execute_command("UPDATE product SET product_inventory = %s WHERE product_id = %s",
                                              [_new_info, product_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "6":
                _result = execute_command("SELECT product_manufactureDate FROM product "
                                          "WHERE product_id = %s", (product_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]

                while True:
                    _new_info = input(f"Please enter your new product manufacture date (old -> {_old_info})\n"
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

                    _result = execute_command("UPDATE product SET product_manufactureDate = %s "
                                              "WHERE product_id = %s",
                                              [_new_info, product_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "7":
                _result = execute_command("SELECT product_description FROM product "
                                          "WHERE product_id = %s", (product_id,))

                if not _result["execute"]:
                    return {"update": False, "message": _result["message"]}

                _old_info = _result["data"][0][0]

                while True:
                    _new_info = input(f"Please enter your new product description (old -> {_old_info})\n"
                                      "If you want it to remain the previous value, enter 0\n>>> ")
                    if _new_info.lower() == "null":
                        print("\n\033[31mYou cannot use the phrase \"null\"\033[0m\n")
                        continue

                    if _new_info == _old_info:
                        print("\n\033[31mWhy??\033[0m\n")
                        continue

                    if _new_info == "0":
                        break

                    _result = execute_command("UPDATE product SET product_description = %s "
                                              "WHERE product_id = %s",
                                              [_new_info, product_id])

                    if not _result["execute"]:
                        return {"update": False, "message": _result["message"]}
                    break
            case "8":
                break
            case _:
                print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                continue
        print(f"\n{_old_info} successfully changed to {_new_info}\n")

    return {"update": True, "message": "information successfully updated"}
