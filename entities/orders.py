from re import findall
from data.currency_units import currency_units
from database.MySQL.execute_command import execute_command
from services.convert_product_price import get_currency_conversion_rate
from services.convert_product_price import convert_product_price
from validator.validating_id import is_valid_uuid4
from validator.validation_quantity import is_valid_quantity


class Orders:
    def __init__(self):
        self._id: str = "null"
        self._customer_id: str = "null"
        self._product_id: str = "null"
        self._quantity: int = 0
        # self._price: str = "null"

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        _result = is_valid_uuid4(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._id = value

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value: str) -> None:
        value = value.strip()

        _result = (execute_command
                   ("SELECT person_id FROM customer WHERE person_id = %s", (value,)))

        if not _result["execute"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        if len(_result["data"]) == 0:
            print("\n\033[31mThe customer ID you entered is not associated "
                  "with any customers in the database\033[0m\n")
            return

        self._customer_id = value

    @property
    def product_id(self) -> str:
        return self._product_id

    @product_id.setter
    def product_id(self, value: str) -> None:
        value = value.strip()

        _result = (execute_command
                   ("SELECT product_id FROM product WHERE product_id = %s", (value,)))

        if not _result["execute"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        if len(_result["data"]) == 0:
            print("\n\033[31mThe product ID you entered is not associated "
                  "with any products in the database\033[0m\n")
            return

        self._product_id = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if self._product_id == "null":
            print("The information is incomplete (product id)\nPlease complete it first and then try again")
            return

        _result = is_valid_quantity(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        _result = (execute_command
                   ("SELECT product_inventory FROM product WHERE product_id = %s", (self._product_id,)))

        if not _result["execute"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        _product_inventory = _result["data"][0][0]
        if _product_inventory < value:
            print("\n\033[31mWe do not have the quantity that you want to order of this product\nPlease enter a "
                  "smaller number\033[0m\n")
            return

        self._quantity = value

    def calculate_price(self) -> dict:
        if self._product_id == "null" or \
                self._quantity == 0:
            return {"calculate": False, "message": "The information is incomplete (product id or quantity)\nPlease "
                                                   "complete it first and then try again"}

        _result = (execute_command
                   ("SELECT product_price FROM product WHERE product_id = %s", (self._product_id,)))

        if not _result["execute"]:
            return {"calculate": False, "message": _result["message"]}

        _product_price = _result["data"][0][0]
        _price_without_currency = float(findall(r"\d+\.?\d*", _product_price)[0])

        _total_price = _price_without_currency * self._quantity

        _result = execute_command("SELECT person.person_region FROM person INNER JOIN employee ON "
                                  "person.person_id = employee.person_id "
                                  "INNER JOIN salesperson ON employee.person_id = salesperson.employee_id "
                                  "WHERE person.person_id = "
                                  "(SELECT product.employee_id FROM product WHERE product_id = %s)",
                                  (self._product_id,))

        if not _result["execute"]:
            return {"calculate": False, "message": _result["message"]}

        _salesperson_region = _result["data"][0][0]

        _result = execute_command("SELECT person.person_region FROM person INNER JOIN customer ON "
                                  "person.person_id = customer.person_id "
                                  "WHERE person.person_id = (SELECT person_id FROM customer WHERE person_id = %s)",
                                  (self._customer_id,))

        if not _result["execute"]:
            return {"calculate": False, "message": _result["message"]}

        _customer_region = _result["data"][0][0]

        _converted_price = ""
        if _salesperson_region == _customer_region:
            _converted_price = f"{currency_units[_customer_region]}{_total_price}"
        else:
            _result = execute_command("SELECT person_id FROM customer WHERE person_id = %s", (self._customer_id,))

            if not _result["execute"]:
                return {"calculate": False, "message": _result["message"]}

            _conversion_rate = get_currency_conversion_rate(_customer_region, _salesperson_region)
            _converted_price = convert_product_price(_total_price, _conversion_rate, self._customer_id)

            _converted_price = _converted_price["data"]

        return {"calculate": True, "data": _converted_price}
