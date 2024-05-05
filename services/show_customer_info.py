from database.MySQL.execute_command import execute_command


def show_customer_info(customer_id: str) -> dict:
    _customer_result = execute_command("SELECT * FROM customer WHERE person_id = %s", (customer_id, ))

    if not _customer_result["execute"]:
        return {"show": False, "message": _customer_result["message"]}

    _person_result = execute_command("SELECT * FROM person WHERE person_id = %s",
                                     (_customer_result["data"][0][0], ))

    if not _person_result["execute"]:
        return {"show": False, "message": _person_result["message"]}

    print("----------------------------------------")
    print(f"First name              ->   {_person_result["data"][0][1]}\n"
          f"Last name               ->   {_person_result["data"][0][2]}\n"
          f"Region                  ->   {_person_result["data"][0][3]}\n"
          f"Phone number            ->   {_person_result["data"][0][4]}\n"
          f"Email                   ->   {_person_result["data"][0][5]}\n"
          f"Date of birth           ->   {_person_result["data"][0][6]}\n"
          f"Gender                  ->   {_person_result["data"][0][7]}\n"
          f"Address                 ->   {_person_result["data"][0][8]}\n"
          f"Username                ->   {_customer_result["data"][0][1]}\n"
          f"Password                ->   {_customer_result["data"][0][2]}\n")

    return {"show": True, "message": "Successfully show customer info"}
