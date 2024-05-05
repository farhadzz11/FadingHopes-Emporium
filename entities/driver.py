from entities.employee import Employee


class Driver(Employee):
    def __init__(self):
        Employee.__init__(self)
        self._license: str = "null"
        self._available_for_freight: bool = True

    @property
    def license(self) -> str:
        return self._license

    @license.setter
    def license(self, value: str) -> None:
        value = value.strip()

        if value not in ("A", "B", "C", "D", "E"):
            print("\n\033[31mThe driver's license class you entered is invalid. Please enter one of the following "
                  "classes:\nENTER A: This class allows you to drive any type of motor vehicle, including cars, "
                  "trucks, and buses\nENTER B: This class allows you to drive cars and trucks, but not buses\nENTER "
                  "C: This class allows you to drive motorcycles and scooters\nENTER D: This class allows you to "
                  "drive taxis and other passenger vehicles\nENTER E: This class allows you to drive vehicles that "
                  "tow trailers\033[0m\n")
            return

        self._license = value

    @property
    def available_for_freight(self) -> bool:
        return self._available_for_freight

    @available_for_freight.setter
    def available_for_freight(self, value: bool) -> None:
        if type(value) is not bool:
            print("\n\033[31mThe value you entered is invalid\n"
                  "The only valid values for this field are True and False\n"
                  "Please enter one of these values\033[0m\n")
            return

        self._available_for_freight = value
