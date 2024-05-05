from re import compile
from datetime import datetime


def is_valid_date(date: str) -> dict:
    _date_pattern = compile(r"^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})$")

    if not _date_pattern.match(date):
        return {"valid": False, "message": f"The format date you entered ({date}) is invalid. Please enter a valid "
                                           f"date in the format YYYY-MM-DD\nOnly dates in the Gregorian calendar are "
                                           f"accepted"}

    _year, _month, _day = date.split('-')

    if not (1899 < int(_year)):
        return {"valid": False,
                "message": f"The year of the date you entered ({_year}) is invalid\nThe year cannot be before 1900"}

    if not (0 < int(_month) < 13):
        return {"valid": False, "message": f"The month of the date you entered ({_month}) is invalid\nThe month must "
                                           f"be between 1 and 12"}

    if not (0 < int(_day) < 32):
        return {"valid": False,
                "message": f"The day of the date you entered ({_day}) is invalid\nThe day must be between 1 and 31"}

    try:
        _date_parsed_datetime = datetime.strptime(date, "%Y-%m-%d")
    except ValueError as error:
        return {"valid": False, "message": error}

    _today = datetime.today()

    if _date_parsed_datetime > _today:
        return {"valid": False,
                "message": f"The date you entered ({date}) is invalid\nThe date cannot be in the future"}

    return {"valid": True, "message": "The date is valid"}

if __name__ == "__main__":
    print(is_valid_date("2023-02-31"))