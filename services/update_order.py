from re import findall
from data.currency_units import currency_units
from database.MySQL.execute_command import execute_command
from services.convert_product_price import get_currency_conversion_rate
from services.convert_product_price import convert_product_price
from validator.validation_quantity import is_valid_quantity


def update_order(customer_id: str) -> dict:
    _result = execute_command("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))

    if not _result["execute"]:
        return {"update": False, "message": _result["message"]}

    if len(_result["data"]) == 0:
        return {"update": False, "message": "\nThere is nothing to delete"}

    while True:
        _order_id = input("\nPlease enter the order id you want to update\n>>> ")

        _result = execute_command("SELECT * FROM orders WHERE orders_id = %s", (_order_id,))

        if not _result["execute"]:
            return {"update": False, "message": _result["message"]}

        if len(_result["data"]) == 0:
            print(f"\033[31m\nOrder id is not valid, Please enter a valid order id\033[0m")
        else:
            break

    _new_quantity = int(input("\nPlease enter the new quantity\n>>> "))
    _result = is_valid_quantity(_new_quantity)

    if not _result["valid"]:
        return {"update": False, "message": _result["message"]}

    _result = execute_command("SELECT orders_quantity FROM orders WHERE orders_id = %s", [_order_id])

    if not _result["execute"]:
        return {"update": False, "message": _result["message"]}

    _order_quantity = _result["data"][0][0]

    _result = execute_command("UPDATE orders SET orders_quantity = %s WHERE orders_id = %s",
                              [_new_quantity, _order_id])

    if not _result["execute"]:
        return {"update": False, "message": _result["message"]}

    _difference = 0

    if _new_quantity > _order_quantity:
        _difference = _new_quantity - _order_quantity
        _op = "-"
    else:
        _difference = _order_quantity - _new_quantity
        _op = "+"

    _result = execute_command(f"UPDATE product SET product_inventory = product_inventory {_op} {_difference} "
                              f"WHERE product_id = (SELECT product_id FROM orders WHERE orders_id = %s)",
                              [_order_id])

    if not _result["execute"]:
        return {"update": False, "message": _result["message"]}

    _result = (execute_command
               ("SELECT product_price FROM product WHERE product_id = "
                "(SELECT product_id FROM orders WHERE orders_id = %s)", (_order_id,)))

    if not _result["execute"]:
        return {"update": False, "message": _result["message"]}

    _product_price = _result["data"][0][0]
    _price_without_currency = float(findall(r"\d+\.?\d*", _product_price)[0])

    _total_price = _price_without_currency * _new_quantity

    _result = execute_command("SELECT person.person_region FROM person INNER JOIN employee ON "
                              "person.person_id = employee.person_id "
                              "INNER JOIN salesperson ON employee.person_id = salesperson.employee_id "
                              "WHERE person.person_id = "
                              "(SELECT product.employee_id FROM product WHERE product_id = "
                              "(SELECT product_id FROM orders WHERE orders_id = %s))",
                              (_order_id,))

    if not _result["execute"]:
        return {"update": False, "message": _result["message"]}

    _salesperson_region = _result["data"][0][0]

    _result = execute_command("SELECT person.person_region FROM person INNER JOIN customer ON "
                              "person.person_id = customer.person_id "
                              "WHERE person.person_id = %s",
                              (customer_id,))

    if not _result["execute"]:
        return {"update": False, "message": _result["message"]}

    _customer_region = _result["data"][0][0]

    _result = execute_command("SELECT person_id FROM customer WHERE person_id = %s", (customer_id,))

    if not _result["execute"]:
        return {"update": False, "message": _result["message"]}

    if _salesperson_region == _customer_region:
        _converted_price = f"{currency_units[_customer_region]}{_total_price}"
    else:
        _conversion_rate = get_currency_conversion_rate(_customer_region, _salesperson_region)
        _converted_price = convert_product_price(_total_price, _conversion_rate, customer_id)

        _converted_price = _converted_price["data"]

    _result = execute_command("UPDATE orders SET orders_price = %s WHERE orders_id = %s",
                              [_converted_price, _order_id])

    if not _result["execute"]:
        return {"update": False, "message": _result["message"]}

    return {"update": True, "message": f"{_order_id} successfully updated"}
