from database.MySQL.execute_command import execute_command
from validator.validation_username import is_valid_username
from validator.validation_password import is_valid_password
from services.initial_setting import initial_setting
from services.login_process import login_process
from services.signup_process import signup_process
from services.show_products import show_products
from services.search_product import search_product
from services.show_orders import show_orders
from services.add_order import add_order
from services.delete_order import delete_order
from services.update_order import update_order
from services.checkout import checkout
from services.update_customer_info import update_customer_info
from services.show_messages import show_messages
from services.show_customers import show_customers
from services.search_customers import search_customers
from services.show_salespersons import show_salespersons
from services.search_salespersons import search_salespersons
from services.add_salesperson import add_salesperson
from services.update_salesperson_info import update_salesperson_info
from services.show_products import show_products_without_set_currency
from services.add_product import add_product
from services.update_product_info import update_product_info
from services.show_drivers import show_drivers
from services.add_driver import add_driver
from services.search_drivers import search_drivers
from services.update_driver_info import update_driver_info


if __name__ == "__main__":
    _user_choice = ""
    _result = ""

    print("Welcome")

    while True:
        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                             "▐   Login            ->     ENTER 1   ▌\n"
                             "▐   Signup           ->     ENTER 2   ▌\n"
                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

        match _user_choice:
            case "1":
                _index = 0
                while True:
                    _index += 1
                    _result = login_process(input("Please enter your username\n>>> "),
                                            input("Please enter your password\n>>> "),
                                            input("Please enter your access level (user of admin)\n>>> "))

                    if _result["login"]:
                        break
                    else:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")

                    if _index == 3:
                        exit("You tried too many times, Bye!")
                break

            case "2":
                _result = signup_process()

                if _result["signup"]:
                    print(f"\nUser with ID {_result["data"]} was successfully registered\n")
                else:
                    exit(f"\n\033[31m{_result["message"]}\033[0m\n")
            case _:
                print("\n\033[31mPlease enter one of the given choices\033[0m\n")

    if (_result["login"] or _result["signup"]) and _result["access_level"] == "user":
        _customer_id = _result["data"][0][0]

        _result_initial_settings = execute_command("SELECT factor_id FROM factor WHERE customer_id = %s "
                                                   "ORDER BY factor_date DESC, factor_time DESC LIMIT 1",
                                                   (_customer_id,))

        if not _result_initial_settings["execute"]:
            exit(_result_initial_settings["message"])

        if len(_result_initial_settings["data"]) != 0:
            _result_initial_settings = initial_setting(_result_initial_settings["data"][0][0])

        _result = execute_command("SELECT person_firstName FROM person "
                                  "INNER JOIN customer ON person.person_id = customer.person_id "
                                  "WHERE person.person_id = %s",
                                  (_customer_id,))

        if not _result["execute"]:
            exit(_result["message"])

        print(f"\nHi, {_result["data"][0][0]}")

        while True:
            _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                 "▐   Show products      ->     ENTER 1   ▌\n"
                                 "▐   My information     ->     ENTER 2   ▌\n"
                                 "▐   My message         ->     ENTER 3   ▌\n"
                                 "▐   Setting            ->     ENTER 4   ▌\n"
                                 "▐   Exit               ->     ENTER 5   ▌\n"
                                 "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

            match _user_choice:
                case "1":
                    _result = show_products(_customer_id)

                    if not _result["show"]:
                        exit(_result["message"])

                    while True:
                        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                             "▐   Search product     ->     ENTER 1   ▌\n"
                                             "▐   My cart            ->     ENTER 2   ▌\n"
                                             "▐   Go back            ->     ENTER 3   ▌\n"
                                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                        if _user_choice == "1":

                            _result = search_product(input("Enter the phrase you want to search for\n>>> "),
                                                     input("In which part should I search for this phrase?\n"
                                                           "(Names: Enter 1, Groups: Enter 2, "
                                                           "Manufacture dates: Enter 3)\n>>> "),
                                                     _customer_id)

                            if not _result["search"]:
                                exit(_result["message"])

                        elif _user_choice == "2":
                            while True:
                                _result = execute_command("SELECT freight_status FROM freight WHERE factor_id = ("
                                                          "SELECT factor_id FROM factor WHERE customer_id = %s "
                                                          "ORDER BY factor_date DESC, factor_time DESC LIMIT 1)",
                                                          (_customer_id,))

                                if not _result["execute"]:
                                    exit(_result["message"])

                                if len(_result["data"]) != 0:
                                    _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                                         "▐   Orders tracking     ->     ENTER 1   ▌\n"
                                                         "▐   Go back             ->     ENTER 2   ▌\n"
                                                         "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                                    if _user_choice == "1":
                                        print(f"The shipping status of your orders status: {_result["data"][0][0]}")
                                        break
                                    elif _user_choice == "2":
                                        break
                                    else:
                                        print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                                        break

                                _result = show_orders(_customer_id)

                                if not _result["show"]:
                                    exit(_result["message"])

                                _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                                     "▐   Add item           ->     ENTER 1   ▌\n"
                                                     "▐   Delete item        ->     ENTER 2   ▌\n"
                                                     "▐   Edit item          ->     ENTER 3   ▌\n"
                                                     "▐   Checkout           ->     ENTER 4   ▌\n"
                                                     "▐   Go back            ->     ENTER 5   ▌\n"
                                                     "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                                match _user_choice:
                                    case "1":
                                        _result = add_order(_customer_id)

                                        if not _result["add"]:
                                            print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                    case "2":
                                        _result = delete_order(_customer_id)

                                        if not _result["delete"]:
                                            print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                    case "3":
                                        _result = update_order(_customer_id)

                                        if not _result["update"]:
                                            print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                    case "4":
                                        _result = checkout(_customer_id)

                                        if not _result["checkout"]:
                                            print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                    case "5":
                                        break
                                    case _:
                                        print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                        elif _user_choice == "3":
                            break
                        else:
                            print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                case "2":
                    _result = update_customer_info(_customer_id)

                    if not _result["update"]:
                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                        continue
                case "3":
                    while True:
                        _result = execute_command("SELECT * FROM message "
                                                  "WHERE customer_id = %s",
                                                  (_customer_id,))

                        if not _result["execute"]:
                            exit(_result["message"])

                        if len(_result["data"]) == 0:
                            print("\n\033[31mNo message found\033[0m\n")
                            break

                        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                             "▐   Show unseen messages      ->     ENTER 1   ▌\n"
                                             "▐   Show all messages         ->     ENTER 2   ▌\n"
                                             "▐   Delete a message          ->     ENTER 3   ▌\n"
                                             "▐   Delete all messages       ->     ENTER 4   ▌\n"
                                             "▐   Go back                   ->     ENTER 5   ▌\n"
                                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                        match _user_choice:
                            case "1":
                                _result = show_messages(_customer_id, True)

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                    continue
                            case "2":
                                _result = show_messages(_customer_id, False)

                                if not _result["show"]:
                                    exit(_result["message"])
                            case "3":
                                while True:
                                    _message_id = input("Please enter the message id\n>>> ")

                                    _result = execute_command("SELECT * FROM message "
                                                              "WHERE customer_id = %s AND message_id = %s",
                                                              [_customer_id, _message_id])

                                    if not _result["execute"]:
                                        exit(_result["message"])

                                    if len(_result["data"]) == 0:
                                        print("\n\033[31mThe message with this ID was not found\033[0m\n")
                                        continue

                                    _result = execute_command("DELETE FROM message "
                                                              "WHERE customer_id = %s AND message_id = %s",
                                                              [_customer_id, _message_id])

                                    if not _result["execute"]:
                                        exit(_result["message"])

                                    print(f"The message with ID {_message_id} was successfully deleted")
                                    break
                            case "4":
                                _result = execute_command("SET sql_safe_updates=0", None)

                                if not _result["execute"]:
                                    exit(_result["message"])

                                _result = execute_command("DELETE FROM message", None)

                                if not _result["execute"]:
                                    exit(_result["message"])

                                print("All messages were deleted")
                                continue
                            case "5":
                                break
                            case _:
                                print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                                continue
                case "4":
                    while True:
                        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                             "▐   Delete account        ->     ENTER 1   ▌\n"
                                             "▐   About shop            ->     ENTER 2   ▌\n"
                                             "▐   Go back               ->     ENTER 3   ▌\n"
                                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                        if _user_choice == "1":
                            _result = execute_command("DELETE FROM person WHERE person_id = %s", _customer_id)

                            if not _result["execute"]:
                                exit(_result["message"])

                            exit("\nPlease restart application\n")
                        elif _user_choice == "2":
                            print("INFORMATION ABOUT SHOP")
                            continue
                        elif _user_choice == "3":
                            break
                        else:
                            print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                            continue
                case "5":
                    exit("BYE")
                case _:
                    print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                    continue
    elif _result["login"] and _result["access_level"] == "admin":
        _admin_id = _result["data"][0][0]
        while True:
            _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                 "▐   Customers          ->        ENTER 1   ▌\n"
                                 "▐   Salespersons       ->        ENTER 2   ▌\n"
                                 "▐   Products           ->        ENTER 3   ▌\n"
                                 "▐   Drivers            ->        ENTER 4   ▌\n"
                                 "▐   Setting            ->        ENTER 5   ▌\n"
                                 "▐   Exit               ->        ENTER 6   ▌\n"
                                 "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

            match _user_choice:
                case "1":
                    while True:
                        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                             "▐   Show customers     ->        ENTER 1   ▌\n"
                                             "▐   Search customers   ->        ENTER 2   ▌\n"
                                             "▐   Add customers      ->        ENTER 3   ▌\n"
                                             "▐   Edit a customer    ->        ENTER 4   ▌\n"
                                             "▐   Delete a customer  ->        ENTER 5   ▌\n"
                                             "▐   Go back            ->        ENTER 6   ▌\n"
                                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                        match _user_choice:
                            case "1":
                                _result = show_customers()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue
                            case "2":
                                _result = search_customers(input("Enter the phrase you want to search for\n>>> "),
                                                           input("In which part should I search for this phrase?\n"
                                                           "(first name: ENTER 1, last name: ENTER 2, region: ENTER 3, "
                                                                 "phone number: ENTER 4, E-mail: ENTER 5, "
                                                                 "username: ENTER 6)\n>>> "))

                                if not _result["search"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue
                            case "3":
                                _result = signup_process()

                                if not _result["signup"]:
                                    exit(_result["message"])
                                else:
                                    print(f"Customer with ID {_result["data"]} has been successfully added")
                            case "4":
                                _result = show_customers()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue

                                while True:
                                    _customer_id = input("\nPlease enter the customer ID of the customer "
                                                         "whose information you want to edit\n>>> ")
                                    _result = execute_command("SELECT person_id FROM customer "
                                                              "WHERE person_id = %s", [_customer_id])

                                    if not _result["execute"]:
                                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                        continue

                                    if len(_result["data"]) == 0:
                                        print(
                                            "\n\033[31mInvalid customer id,\nPlease enter a valid customer ID\033[0m\n")
                                        continue
                                    else:
                                        break

                                _result = update_customer_info(_customer_id)

                                if not _result["update"]:
                                    exit(_result["message"])
                            case "5":
                                _result = show_customers()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue

                                while True:
                                    _customer_id = input("\nPlease enter the customer ID you want to delete\n>>> ")
                                    _result = execute_command("SELECT person_id FROM customer "
                                                              "WHERE person_id = %s", [_customer_id])

                                    if not _result["execute"]:
                                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                        continue

                                    if len(_result["data"]) == 0:
                                        print(
                                            "\n\033[31mInvalid customer id,\nPlease enter a valid customer ID\033[0m\n")
                                        continue
                                    else:
                                        break

                                _result = execute_command("DELETE FROM person "
                                                          "WHERE person_id = %s", [_customer_id])

                                if not _result["execute"]:
                                    print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                    continue

                                print(f"\ncustomer with ID {_customer_id} has been successfully deleted")

                            case "6":
                                break
                            case _:
                                print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                case "2":
                    while True:
                        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                             "▐   Show salespersons       ->        ENTER 1   ▌\n"
                                             "▐   Search salespersons     ->        ENTER 2   ▌\n"
                                             "▐   Add a salespersons      ->        ENTER 3   ▌\n"
                                             "▐   Edit a salespersons     ->        ENTER 4   ▌\n"
                                             "▐   Delete a salespersons   ->        ENTER 5   ▌\n"
                                             "▐   Go back                 ->        ENTER 6   ▌\n"
                                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                        match _user_choice:
                            case "1":
                                _result = show_salespersons()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue
                            case "2":
                                _result = search_salespersons(input("Enter the phrase you want to search for\n>>> "),
                                                              input("In which part should I search for this phrase?\n"
                                                                    "(first name: ENTER 1, last name: ENTER 2,"
                                                                    "region: ENTER 3, "
                                                                    "phone number: ENTER 4, E-mail: ENTER 5, "
                                                                    "date of hire: ENTER 6, eduction: ENTER 7)\n>>> "))

                                if not _result["search"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue
                            case "3":
                                _result = add_salesperson()

                                if not _result["add"]:
                                    exit(_result["message"])
                                else:
                                    print(f"Salesperson with ID {_result["data"]} has been successfully added")
                            case "4":
                                _result = show_salespersons()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue

                                while True:
                                    _salesperson_id = input("\nPlease enter the salesperson ID of the salespersons "
                                                            "whose information you want to edit\n>>> ")
                                    _result = execute_command("SELECT employee_id FROM salesperson "
                                                              "WHERE employee_id = %s", [_salesperson_id])

                                    if not _result["execute"]:
                                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                        continue

                                    if len(_result["data"]) == 0:
                                        print(
                                            "\n\033[31mInvalid salesperson id,"
                                            "\nPlease enter a valid salesperson ID\033[0m\n")
                                        continue
                                    else:
                                        break

                                _result = update_salesperson_info(_salesperson_id)

                                if not _result["update"]:
                                    exit(_result["message"])
                            case "5":
                                _result = show_salespersons()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue

                                while True:
                                    _salesperson_id = input("\nPlease enter the salesperson ID you want to delete\n>>>")
                                    _result = execute_command("SELECT employee_id FROM salesperson "
                                                              "WHERE employee_id = %s", [_salesperson_id])

                                    if not _result["execute"]:
                                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                        continue

                                    if len(_result["data"]) == 0:
                                        print(
                                            "\n\033[31mInvalid salesperson id,"
                                            "\nPlease enter a valid salesperson ID\033[0m\n")
                                        continue
                                    else:
                                        break

                                _result = execute_command("DELETE FROM person "
                                                          "WHERE person_id = %s", [_salesperson_id])

                                if not _result["execute"]:
                                    print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                    continue

                                print(f"\nsalesperson with ID {_salesperson_id} has been successfully deleted")
                            case "6":
                                break
                            case _:
                                print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                case "3":
                    while True:
                        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                             "▐   Show products           ->        ENTER 1   ▌\n"
                                             "▐   Search products         ->        ENTER 2   ▌\n"
                                             "▐   Add a product           ->        ENTER 3   ▌\n"
                                             "▐   Edit a product          ->        ENTER 4   ▌\n"
                                             "▐   Delete a product        ->        ENTER 5   ▌\n"
                                             "▐   Go back                 ->        ENTER 6   ▌\n"
                                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                        match _user_choice:
                            case "1":
                                _result = show_products_without_set_currency()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue
                            case "2":
                                while True:
                                    _customer_id = input(
                                        "\nPlease enter the customer ID to "
                                        "fetch the currency and display it with that currency.\n>>> ")

                                    _result = execute_command("SELECT * FROM customer WHERE person_id = %s",
                                                              [_customer_id])

                                    if not _result["execute"]:
                                        exit(_result["message"])

                                    if len(_result["data"]) != 0:
                                        break

                                _result = search_product(input("Enter the phrase you want to search for\n>>> "),
                                                         input("In which part should I search for this phrase?\n"
                                                               "(Names: Enter 1, Groups: Enter 2, "
                                                               "Manufacture dates: Enter 3)\n>>> "),
                                                         _customer_id)

                                if not _result["search"]:
                                    print(_result["message"])
                                    continue
                            case "3":
                                _result = add_product()

                                if not _result["add"]:
                                    exit(_result["message"])
                                else:
                                    print(f"Product with ID {_result["data"]} has been successfully added")
                            case "4":
                                _result = show_products_without_set_currency()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue

                                while True:
                                    _product_id = input("\nPlease enter the product ID of the products "
                                                        "whose information you want to edit\n>>> ")
                                    _result = execute_command("SELECT * FROM product "
                                                              "WHERE product_id = %s", [_product_id])

                                    if not _result["execute"]:
                                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                        continue

                                    if len(_result["data"]) == 0:
                                        print(
                                            "\n\033[31mInvalid product id,"
                                            "\nPlease enter a valid product ID\033[0m\n")
                                        continue
                                    else:
                                        break

                                _result = update_product_info(_product_id)

                                if not _result["update"]:
                                    exit(_result["message"])
                            case "5":
                                _result = show_products_without_set_currency()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue

                                while True:
                                    _product_id = input(
                                        "\nPlease enter the product ID you want to delete\n>>> ")
                                    _result = execute_command("SELECT * FROM product "
                                                              "WHERE product_id = %s", [_product_id])

                                    if not _result["execute"]:
                                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                        continue

                                    if len(_result["data"]) == 0:
                                        print(
                                            "\n\033[31mInvalid product id,"
                                            "\nPlease enter a valid product ID\033[0m\n")
                                        continue
                                    else:
                                        break

                                _result = execute_command("DELETE FROM product "
                                                          "WHERE product_id = %s", [_product_id])

                                if not _result["execute"]:
                                    print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                    continue

                                print(f"\nproduct with ID {_product_id} has been successfully deleted")
                            case "6":
                                break
                            case _:
                                print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                case "4":
                    while True:
                        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                             "▐   Show drivers            ->        ENTER 1   ▌\n"
                                             "▐   Search drivers          ->        ENTER 2   ▌\n"
                                             "▐   Add a driver            ->        ENTER 3   ▌\n"
                                             "▐   Edit a driver           ->        ENTER 4   ▌\n"
                                             "▐   Delete a driver         ->        ENTER 5   ▌\n"
                                             "▐   Go back                 ->        ENTER 6   ▌\n"
                                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                        match _user_choice:
                            case "1":
                                _result = show_drivers()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue
                            case "2":
                                _result = search_drivers(input("Enter the phrase you want to search for\n>>> "),
                                                         input("In which part should I search for this phrase?\n"
                                                               "(first name: ENTER 1, last name: ENTER 2,"
                                                               "region: ENTER 3, "
                                                               "phone number: ENTER 4, E-mail: ENTER 5, "
                                                               "date of hire: ENTER 6, eduction: ENTER 7"
                                                               "license: ENTER 8)\n>>> "))

                                if not _result["search"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue
                            case "3":
                                _result = add_driver()

                                if not _result["add"]:
                                    exit(_result["message"])
                                else:
                                    print(f"Driver with ID {_result["data"]} has been successfully added")
                            case "4":
                                _result = show_drivers()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue

                                while True:
                                    _driver_id = input("\nPlease enter the driver ID of the drivers "
                                                       "whose information you want to edit\n>>> ")
                                    _result = execute_command("SELECT employee_id FROM driver "
                                                              "WHERE employee_id = %s", [_driver_id])

                                    if not _result["execute"]:
                                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                        continue

                                    if len(_result["data"]) == 0:
                                        print(
                                            "\n\033[31mInvalid driver id,"
                                            "\nPlease enter a valid driver ID\033[0m\n")
                                        continue
                                    else:
                                        break

                                _result = update_driver_info(_driver_id)

                                if not _result["update"]:
                                    exit(_result["message"])
                            case "5":
                                _result = show_drivers()

                                if not _result["show"]:
                                    print(f"\n\033[31m{_result["message"]}\n\033[0m")
                                    continue

                                while True:
                                    _driver_id = input(
                                        "\nPlease enter the driver ID you want to delete\n>>> ")
                                    _result = execute_command("SELECT employee_id FROM driver "
                                                              "WHERE employee_id = %s", [_driver_id])

                                    if not _result["execute"]:
                                        print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                        continue

                                    if len(_result["data"]) == 0:
                                        print(
                                            "\n\033[31mInvalid driver id,"
                                            "\nPlease enter a valid driver ID\033[0m\n")
                                        continue
                                    else:
                                        break

                                _result = execute_command("DELETE FROM person "
                                                          "WHERE person_id = %s", [_driver_id])

                                if not _result["execute"]:
                                    print(f"\n\033[31m{_result["message"]}\033[0m\n")
                                    continue

                                print(f"\ndriver with ID {_driver_id} has been successfully deleted")
                            case "6":
                                break
                            case _:
                                print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                case "5":
                    while True:
                        _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                             "▐   Change my information     ->     ENTER 1   ▌\n"
                                             "▐   Delete account            ->     ENTER 2   ▌\n"
                                             "▐   Go back                   ->     ENTER 3   ▌\n"
                                             "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                        if _user_choice == "1":
                            while True:
                                _user_choice = input("▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n"
                                                     "▐   Change username           ->     ENTER 1   ▌\n"
                                                     "▐   Change password           ->     ENTER 2   ▌\n"
                                                     "▐   Go back                   ->     ENTER 3   ▌\n"
                                                     "▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n>>> ")

                                if _user_choice == "1":
                                    _result = execute_command("SELECT admin_username FROM admins "
                                                              "WHERE admin_id = %s",
                                                              (_admin_id,))

                                    if not _result["execute"]:
                                        exit(_result["message"])

                                    _old_info = _result["data"][0][0]
                                    _new_info = ""
                                    while True:
                                        _new_info = input(f"Please enter your new username -> old ({_old_info})\n"
                                                          "If you want it to remain the previous value, "
                                                          "enter 0\n>>> ")
                                        if _new_info.lower() == "unknown":
                                            print("You cannot use the phrase \"Unknown\"")
                                            continue

                                        if _new_info == "0":
                                            break

                                        _result = is_valid_username(_new_info)

                                        if not _result["valid"]:
                                            print(f"\033[31m\n{_result["message"]}\033[0m\n")
                                        else:
                                            break
                                    _result = execute_command("UPDATE admins SET admin_username = %s "
                                                              "WHERE admin_id = %s",
                                                              [_new_info, _admin_id])

                                    if not _result["execute"]:
                                        exit(_result["message"])

                                    print(f"\n{_old_info} successfully changed to {_new_info}\n")
                                elif _user_choice == "2":
                                    _result = execute_command("SELECT admin_password FROM admins "
                                                              "WHERE admin_id = %s",
                                                              (_admin_id,))

                                    if not _result["execute"]:
                                        exit(_result["message"])

                                    _old_info = _result["data"][0][0]
                                    _new_info = ""
                                    while True:
                                        _new_info = input(f"Please enter your new password -> old ({_old_info})\n"
                                                          "If you want it to remain the previous value, "
                                                          "enter 0\n>>> ")
                                        if _new_info.lower() == "unknown":
                                            print("You cannot use the phrase \"Unknown\"")
                                            continue

                                        if _new_info == "0":
                                            break

                                        _result = is_valid_password(_new_info)

                                        if not _result["valid"]:
                                            print(f"\033[31m\n{_result["message"]}\033[0m\n")
                                        else:
                                            break
                                    _result = execute_command("UPDATE admins SET admin_password = %s "
                                                              "WHERE admin_id = %s",
                                                              [_new_info, _admin_id])

                                    if not _result["execute"]:
                                        exit(_result["message"])

                                    print(f"\n{_old_info} successfully changed to {_new_info}\n")
                                elif _user_choice == "3":
                                    break
                                else:
                                    print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                        elif _user_choice == "2":
                            _result = execute_command("DELETE FROM admins "
                                                      "WHERE admin_id = %s",
                                                      (_admin_id,))

                            if not _result["execute"]:
                                exit(_result["message"])

                            exit("YOUR ACCOUNT HAS BEEN SUCCESSFULLY DELETED, PLEASE RESTART THE APP")
                        elif _user_choice == "3":
                            break
                        else:
                            print("\n\033[31mPlease enter one of the given choices\033[0m\n")
                case "6":
                    exit("BYE ADMIN")
                case _:
                    print("\n\033[31mPlease enter one of the given choices\033[0m\n")
