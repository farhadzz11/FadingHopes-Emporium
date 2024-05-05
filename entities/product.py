from data.product_groups import product_groups
from data.currency_units import currency_units
from database.MySQL.execute_command import execute_command
from validator.validating_id import is_valid_uuid4
from validator.validation_product_name import is_valid_product_name
from validator.validation_price import is_valid_price
from validator.validation_inventory import is_valid_inventory
from validator.validation_date import is_valid_date


class Product:
    def __init__(self):
        self._id: str = "null"
        self._salesperson_id: str = "null"
        self._name: str = "null"
        self._group: str = "null"
        self._price: str = "null"
        self._inventory: int = 0
        self._manufacture_date: str = "null"
        self._description: str = "null"

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
    def salesperson_id(self) -> str:
        return self._salesperson_id

    @salesperson_id.setter
    def salesperson_id(self, value: str) -> None:
        value = value.strip()

        _result = execute_command("SELECT person.person_id FROM person INNER JOIN employee ON "
                                  "person.person_id = employee.person_id "
                                  "INNER JOIN salesperson ON employee.person_id = salesperson.employee_id "
                                  "WHERE person.person_id = %s", (value, ))

        if not _result["execute"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        if len(_result["data"]) == 0:
            print(f"\n\033[31mThe salesperson ID you entered is not associated "
                  f"with any salespersons in the database\033[0m\n")
            return

        self._salesperson_id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_product_name(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._name = value

    @property
    def group(self) -> str:
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        value = value.strip()

        if value.lower() not in product_groups:
            print("\n\033[31mThe product group is invalid\nThe product group must be one of the following: \n"
                  f"{product_groups}\033[0m\n")
            return

        self._group = value

    @property
    def price(self) -> str:
        return self._price

    @price.setter
    def price(self, value: str) -> None:
        value = value.strip()

        if self._salesperson_id == "null":
            print("\n\033[31mThe salesperson id field cannot be empty\nPlease enter it first\033[0m\n")
            return

        _result = execute_command("SELECT person.person_region FROM person INNER JOIN employee ON "
                                  "person.person_id = employee.person_id "
                                  "INNER JOIN salesperson ON employee.person_id = salesperson.employee_id "
                                  "WHERE person.person_id = %s", (self._salesperson_id,))

        if not _result["execute"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        _region = _result["data"][0][0]

        _result = is_valid_price(value, _region)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._price = f"{currency_units[_region]}{value}"

    @property
    def inventory(self) -> int:
        return self._inventory

    @inventory.setter
    def inventory(self, value: int) -> None:
        _result = is_valid_inventory(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._inventory = value

    @property
    def manufacture_date(self) -> str:
        return self._manufacture_date

    @manufacture_date.setter
    def manufacture_date(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_date(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._manufacture_date = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

