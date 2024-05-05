from database.MySQL.execute_command import execute_command


def show_customers() -> dict:
    _result = execute_command("SELECT person.*, customer.customer_username, customer.customer_password FROM person "
                              "INNER JOIN customer ON person.person_id = customer.person_id", None)

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    if len(_result["data"]) == 0:
        return {"show": False, "message": "There is no customer to show"}

    for row in _result["data"]:
        print("----------------------------------------")
        print(f"Customer ID = {row[0]}\n"
              f"Customer first name         ->   {row[1]}\n"
              f"Customer last name          ->   {row[2]}\n"
              f"Customer region             ->   {row[3]}\n"
              f"Customer phone number       ->   {row[4]}\n"
              f"Customer E-mail             ->   {row[5]}\n"
              f"Customer date of birth      ->   {row[6]}\n"
              f"Customer gender             ->   {row[7]}\n"
              f"Customer address            ->   {row[8]}\n"
              f"Customer description        ->   {row[9]}\n"
              f"Customer username           ->   {row[10]}\n"
              f"Customer password           ->   {row[11]}\n")

    return {"show": True, "message": "All customers were displayed"}


def show_a_customer(customer_id: str) -> dict:
    _result = execute_command("SELECT person.*, customer.customer_username, customer.customer_password FROM person "
                              "INNER JOIN customer ON person.person_id = customer.person_id "
                              "WHERE customer.person_id = %s", (customer_id,))

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    print("----------------------------------------")
    print(f"Customer ID = {_result["data"][0][0]}\n"
          f"Customer first name         ->   {_result["data"][0][1]}\n"
          f"Customer last name          ->   {_result["data"][0][2]}\n"
          f"Customer region             ->   {_result["data"][0][3]}\n"
          f"Customer phone number       ->   {_result["data"][0][4]}\n"
          f"Customer E-mail             ->   {_result["data"][0][5]}\n"
          f"Customer date of birth      ->   {_result["data"][0][6]}\n"
          f"Customer gender             ->   {_result["data"][0][7]}\n"
          f"Customer address            ->   {_result["data"][0][8]}\n"
          f"Customer description        ->   {_result["data"][0][9]}\n"
          f"Customer username           ->   {_result["data"][0][10]}\n"
          f"Customer password           ->   {_result["data"][0][11]}\n")

    return {"show": True, "message": "customer was displayed"}
