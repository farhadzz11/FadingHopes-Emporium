from re import findall
from database.MySQL.execute_command import execute_command
from services.convert_product_price import get_currency_conversion_rate
from services.convert_product_price import convert_product_price


def search_product(phrase: str, search_by: str, customer_id: str) -> dict:
    _result = execute_command("SELECT person.person_region FROM person INNER JOIN customer ON "
                              "person.person_id = customer.person_id "
                              "WHERE person.person_id = %s",
                              (customer_id,))

    if not _result["execute"]:
        return {"search": False, "message": _result["message"]}

    _customer_region = _result["data"][0][0]

    _value_search_by = ""

    if search_by == "1":
        _value_search_by = "product_name"
    elif search_by == "2":
        _value_search_by = "product_group"
    elif search_by == "3":
        _value_search_by = "product_manufactureDate"
    else:
        return {"search": False, "message": "Please enter one of the given choices"}

    _result = execute_command(f"SELECT * FROM product WHERE {_value_search_by} LIKE '{phrase}%'", None)

    if not _result["execute"]:
        return {"search": False, "message": _result["message"]}

    _all_information = _result["data"]

    for _information in _all_information:
        _result = execute_command("SELECT person_region FROM person "
                                  "INNER JOIN customer ON person.person_id = customer.person_id "
                                  "WHERE person.person_id = %s",
                                  (customer_id,))

        if not _result["execute"]:
            return {"search": False, "message": _result["message"]}

        _customer_region = _result["data"][0][0]

        _result = execute_command("SELECT person.person_region FROM person INNER JOIN employee ON "
                                  "person.person_id = employee.person_id "
                                  "INNER JOIN salesperson ON employee.person_id = salesperson.employee_id "
                                  "WHERE person.person_id = "
                                  "(SELECT product.employee_id FROM product WHERE product_id = %s)",
                                  (_information[0],))

        if not _result["execute"]:
            return {"search": False, "message": _result["message"]}

        _salesperson_region = _result["data"][0][0]

        if _customer_region == _salesperson_region:
            _converted_price = _information[4]
        else:
            _conversion_rate = get_currency_conversion_rate(_customer_region, _salesperson_region)

            _price_without_currency = float(findall(r"\d+\.?\d*", _information[4])[0])

            _converted_price = convert_product_price(_price_without_currency, _conversion_rate, customer_id)

            _converted_price = _converted_price["data"]

        print("----------------------------------------")
        print(f"Product ID = {_information[0]}\n"
              f"Product name                   ->   {_information[2]}\n"
              f"Product group                  ->   {_information[3]}\n"
              f"Product price                  ->   {_converted_price}\n"
              f"Product inventory              ->   {_information[5]}\n"
              f"Product manufacture date       ->   {_information[6]}\n")

    return {"search": True, "message": "All products were displayed"}
