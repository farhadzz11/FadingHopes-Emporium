from database.MySQL.execute_command import execute_command
from services.show_customers import show_a_customer


def search_customers(phrase: str, search_by: str) -> dict:
    _value_search_by = ""

    if search_by == "1":
        _value_search_by = "person.person_firstName"
    elif search_by == "2":
        _value_search_by = "person.person_lastName"
    elif search_by == "3":
        _value_search_by = "person.person_region"
    elif search_by == "4":
        _value_search_by = "person.person_phoneNumber"
    elif search_by == "5":
        _value_search_by = "person.person_email"
    elif search_by == "6":
        _value_search_by = "customer.customer_username"
    else:
        return {"search": False, "message": "Please enter one of the given choices"}

    _result = execute_command("SELECT person.*, customer.customer_username, customer.customer_password FROM person "
                              "INNER JOIN customer ON person.person_id = customer.person_id "
                              f"WHERE {_value_search_by} LIKE '{phrase}%'", None)

    if not _result["execute"]:
        return {"search": False, "message": _result["message"]}

    if len(_result["data"]) == 0:
        return {"search": False, "message": "No customer found for the given phrase"}

    for row in _result["data"]:
        show_a_customer(row[0])

    return {"search": True, "message": "All customers were displayed"}
