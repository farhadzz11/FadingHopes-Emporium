from database.MySQL.execute_command import execute_command
from validator.validating_id import is_valid_uuid4
from validator.validation_date import is_valid_date
from validator.validation_time import is_valid_time


class Freight:
    def __init__(self):
        self._id: str = "null"
        self._factor_id: str = "null"
        self._driver_id: str = "null"
        self._status: str = "null"
        self._departure_date: str = "null"
        self._departure_time: str = "null"

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
    def factor_id(self) -> str:
        return self._factor_id

    @factor_id.setter
    def factor_id(self, value: str) -> None:
        value = value.strip()

        _result = (execute_command
                   ("SELECT factor_id FROM factor WHERE factor_id = %s", (value,)))

        if not _result["execute"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        if len(_result["data"]) == 0:
            print("\n\033[31mThe factor ID you entered is not associated "
                  "with any factors in the database\033[0m\n")
            return

        self._factor_id = value

    @property
    def driver_id(self) -> str:
        return self._driver_id

    @driver_id.setter
    def driver_id(self, value: str) -> None:
        value = value.strip()

        _result = (execute_command
                   ("SELECT employee_id FROM driver WHERE employee_id = %s", (value,)))

        if not _result["execute"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        if len(_result["data"]) == 0:
            print("\n\033[31mThe driver ID you entered is not associated "
                  "with any drivers in the database\033[0m\n")
            return

        self._driver_id = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        if value.lower() not in ("loading", "unshipped", "in transit", "shipped", "customer unavailable for delivery"):
            print("The entered freight status is invalid\nPlease enter one of the terms below: loading or unshipped "
                  "or in transit or shipped or customer unavailable for delivery")
            return

        self._status = value

    @property
    def departure_date(self) -> str:
        return self._departure_date

    @departure_date.setter
    def departure_date(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_date(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._departure_date = value

    @property
    def departure_time(self) -> str:
        return self._departure_time

    @departure_time.setter
    def departure_time(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_time(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._departure_time = value
