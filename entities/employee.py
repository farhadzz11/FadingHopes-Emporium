from data.academic_degrees import academic_degrees
from entities.person import Person
from validator.validation_date import is_valid_date
from validator.validation_work_experience import is_valid_work_experience


class Employee(Person):
    def __init__(self):
        Person.__init__(self)
        self._date_of_hire: str = "null"
        self._education: str = "null"
        self._work_experience: list = []
        self._legal_information: str = "null"

    @property
    def date_of_hire(self) -> str:
        return self._date_of_hire

    @date_of_hire.setter
    def date_of_hire(self, value: str) -> None:
        value = value.strip()

        _result = is_valid_date(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._date_of_hire = value

    @property
    def education(self) -> str:
        return self._education

    @education.setter
    def education(self, value: str) -> None:
        value = value.strip()

        if value not in academic_degrees:
            print("\n\033[31mThe education you entered is invalid. Please select an education from the following "
                  f"list\n{academic_degrees}\033[0m\n")
            return

        self._education = value

    @property
    def work_experience(self) -> list:
        return self._work_experience

    @work_experience.setter
    def work_experience(self, value: list) -> None:
        # The input format for work experience should be as follows:
        # ["company name", "job title", "start date", "end date", "description"]

        _result = is_valid_work_experience(value)

        if not _result["valid"]:
            print(f"\n\033[31m{_result["message"]}\033[0m\n")
            return

        self._work_experience = value

    @property
    def legal_information(self) -> str:
        return self._legal_information

    @legal_information.setter
    def legal_information(self, value: str) -> None:
        if not (0 <= len(value) <= 255):
            print("\n\033[31mThe legal information must be between 0 and 255 characters long\033[0m\n")
            return

        self._legal_information = value
