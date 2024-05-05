from re import findall
from data.currency_units import currency_units
from database.MySQL.execute_command import execute_command
from validator.validating_id import is_valid_uuid4
from validator.validation_date import is_valid_date
from validator.validation_time import is_valid_time


class Factor:
    def __init__(self):
        self._id: str = "null"
        self._customer_id: str = "null"
        # self._total_price: str = "null"
        self._payment_status: str = "null"
        self._date: str = "null"
        self._time: str = "null"

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

    def calculate_total_price(self) -> dict:
        if self.customer_id == "null":
            return {"calculate": False, "message": "The information is incomplete\nPlease complete it first and then "
                                                   "try again"}

        _result = execute_command("SELECT orders_id FROM orders WHERE customer_id = %s", (self._customer_id,))

        if not _result["execute"]:
            return {"calculate": False, "message": _result["message"]}

        _order_ids = _result["data"]
        _total_price = 0
        for _order_id in _order_ids:
            _result = execute_command("SELECT orders_price FROM orders WHERE orders_id = %s", (_order_id[0],))

            if not _result["execute"]:
                return {"calculate": False, "message": _result["message"]}

            _product_price = _result["data"][0][0]
            _price_without_currency = float(findall(r"\d+\.?\d*", _product_price)[0])

            _total_price += _price_without_currency

        _result = execute_command("SELECT person.person_region FROM person INNER JOIN customer ON "
                                  "person.person_id = customer.person_id "
                                  "WHERE person.person_id = %s",
                                  (self._customer_id, ))

        if not _result["execute"]:
            return {"calculate": False, "message": _result["message"]}

        _customer_region = _result["data"][0][0]

        return {"calculate": True, "data": f"{currency_units[_customer_region]}{_total_price}"}

    @property
    def payment_status(self) -> str:
        return self._payment_status

    @payment_status.setter
    def payment_status(self, value: str) -> None:
        if value.lower() not in ("unpaid", "paid", "undetermined"):
            print("The entered payment status is invalid\nPlease enter one of the terms below: unpaid or paid or "
                  "undetermined")
            return

        self._payment_status = value

    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_date(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._date = value

    @property
    def time(self) -> str:
        return self._time

    @time.setter
    def time(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_time(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._time = value
