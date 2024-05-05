from entities.person import Person
from database.MySQL.execute_command import execute_command
from validator.validation_username import is_valid_username
from validator.validation_password import is_valid_password


class Customer(Person):
    def __init__(self):
        Person.__init__(self)
        self._username: str = "null"
        self._password: str = "null"

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_username(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        _result = execute_command("SELECT customer_username FROM customer WHERE customer_username = %s", (value,))

        if not _result["execute"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        if len(_result["data"]) != 0:
            print(f"\n\033[31mThe username already exists\nPlease enter another username\033[0m\n")
            return

        self._username = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        _result = is_valid_password(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._password = value
