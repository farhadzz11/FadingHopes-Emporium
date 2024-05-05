from re import findall
from database.MySQL.execute_command import execute_command
from services.convert_product_price import get_currency_conversion_rate
from services.convert_product_price import convert_product_price


def show_products(customer_id: str) -> dict:
    _result = execute_command("SELECT * FROM product", None)

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    for product in _result["data"]:
        _result = execute_command("SELECT person_region FROM person "
                                  "INNER JOIN customer ON person.person_id = customer.person_id "
                                  "WHERE person.person_id = %s",
                                  (customer_id,))

        if not _result["execute"]:
            return {"show": False, "message": _result["message"]}

        _customer_region = _result["data"][0][0]

        _result = execute_command("SELECT person.person_region FROM person INNER JOIN employee ON "
                                  "person.person_id = employee.person_id "
                                  "INNER JOIN salesperson ON employee.person_id = salesperson.employee_id "
                                  "WHERE person.person_id = "
                                  "(SELECT product.employee_id FROM product WHERE product_id = %s)",
                                  (product[0],))

        if not _result["execute"]:
            return {"show": False, "message": _result["message"]}

        _salesperson_region = _result["data"][0][0]

        if _customer_region == _salesperson_region:
            _converted_price = product[4]
        else:
            _conversion_rate = get_currency_conversion_rate(_customer_region, _salesperson_region)

            _price_without_currency = float(findall(r"\d+\.?\d*", product[4])[0])

            _converted_price = convert_product_price(_price_without_currency, _conversion_rate, customer_id)["data"]

        print("----------------------------------------")
        print(f"Product ID = {product[0]}\n"
              f"Product name                   ->   {product[2]}\n"
              f"Product group                  ->   {product[3]}\n"
              f"Product price                  ->   {_converted_price}\n"
              f"Product inventory              ->   {product[5]}\n"
              f"Product manufacture date       ->   {product[6]}\n")

    return {"show": True, "message": "All products were displayed"}


def show_products_without_set_currency():
    _result = execute_command("SELECT * FROM product", None)

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    if len(_result["data"]) == 0:
        return {"show": False, "message": "There is no product to show"}

    for product in _result["data"]:
        print("----------------------------------------")
        print(f"Product ID = {product[0]}\n"
              f"Product salesperson id         ->   {product[1]}\n"
              f"Product name                   ->   {product[2]}\n"
              f"Product group                  ->   {product[3]}\n"
              f"Product price                  ->   {product[4]}\n"
              f"Product inventory              ->   {product[5]}\n"
              f"Product manufacture date       ->   {product[6]}\n"
              f"Product description            ->   {product[7]}\n")

    return {"show": True, "message": "All products were displayed"}


def show_a_product(product_id: str) -> dict:
    _result = execute_command("SELECT * FROM product WHERE product_id = %s", [product_id])

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    print("----------------------------------------")
    print(f"Product ID = {_result["data"][0][0]}\n"
          f"Product salesperson id         ->   {_result["data"][0][1]}\n"
          f"Product name                   ->   {_result["data"][0][2]}\n"
          f"Product group                  ->   {_result["data"][0][3]}\n"
          f"Product price                  ->   {_result["data"][0][4]}\n"
          f"Product inventory              ->   {_result["data"][0][5]}\n"
          f"Product manufacture date       ->   {_result["data"][0][6]}\n"
          f"Product description            ->   {_result["data"][0][7]}\n")

    return {"show": True, "message": "The product was displayed"}
