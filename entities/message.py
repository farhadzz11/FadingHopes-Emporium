from database.MySQL.execute_command import execute_command
from validator.validating_id import is_valid_uuid4
from validator.validation_date import is_valid_date
from validator.validation_time import is_valid_time


class Message:
    def __init__(self):
        self._id: str = "null"
        self._customer_id: str = "null"
        self._txt: str = "null"
        self._date: str = "null"
        self._time: str = "null"
        self._seen: bool = False

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
    def txt(self) -> str:
        return self._txt

    @txt.setter
    def txt(self, value: str) -> None:
        if not (0 < len(value) < 129):
            print("The text you entered is too long or too short\nThe maximum length is 128 characters and the "
                  "minimum length is 2 characters")
            return

        self._txt = value

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

    @property
    def seen(self) -> bool:
        return self._seen

    @seen.setter
    def seen(self, value: bool) -> None:
        if type(value) is not bool:
            print(f"\n\033[31mValue must be True or False, Please enter a valid value\033[0m\n")
            return

        self._seen = value
