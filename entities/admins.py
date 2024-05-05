from validator.validating_id import is_valid_uuid4
from validator.validation_username import is_valid_username
from validator.validation_password import is_valid_password


class Admins:
    def __init__(self):
        self._id: str = "null"
        self._username: str = "null"
        self._password: str = "null"

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
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_username(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
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
