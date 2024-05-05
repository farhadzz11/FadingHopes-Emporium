from data.regions import regions
from services.parse_phone_region import parse_phone_region
from validator.validating_id import is_valid_uuid4
from validator.validation_name import is_valid_name
from validator.validating_phone_number import is_valid_phone_number
from validator.validation_email import is_valid_email
from validator.validation_date import is_valid_date
from validator.validation_address import is_valid_address


class Person:
    def __init__(self):
        self._id: str = "null"
        self._first_name: str = "null"
        self._last_name: str = "null"
        self._region: str = "null"
        self._phone_number: str = "null"
        self._email: str = "null"
        self._date_of_birth: str = "null"
        self._gender: str = "null"
        self._address: str = "null"
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
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_name(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._first_name = value

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_name(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._last_name = value

    @property
    def region(self) -> str:
        return self._region

    @region.setter
    def region(self, value: str) -> None:
        value = value.strip()

        if value not in regions.keys():
            print("\n\033[31mThe region code is invalid\nThe region code must be a two-letter code that identifies "
                  "the country\nThe following are the countries supported in this program, "
                  f"along with their country codes\n{regions.keys()}\033[0m\n")
            return

        self._region = value

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: str) -> None:
        value = value.strip()

        if self.region == "null":
            print("\n\033[31mThe region field cannot be empty\n"
                  "Please enter it first\033[0m\n")
            return

        if value.startswith("0"):
            value = value[1:]

        _result = is_valid_phone_number(value, self.region)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._phone_number = f"+{parse_phone_region(value, self._region)}{value}"

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_email(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._email = value

    @property
    def date_of_birth(self) -> str:
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_date(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._date_of_birth = value

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str) -> None:
        value = value.strip()

        if value not in ("male", "female"):
            print("\n\033[31mThe gender you entered is invalid.\nPlease enter either \"male\" or \"female\"\033[0m\n")
            return

        self._gender = value

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_address(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._address = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value
