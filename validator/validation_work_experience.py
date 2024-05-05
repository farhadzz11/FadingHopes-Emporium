from datetime import datetime
from re import compile
from data.offensive_words import offensive_words
from validator.validation_date import is_valid_date


def is_valid_work_experience(work_experience: list[str]) -> dict:
    if not isinstance(work_experience, list) or len(work_experience) != 5:
        return _return_exception("Invalid data structure for work experience")

    _company_job_pattern = compile(r"^[a-zA-Z0-9\s]{5,30}$")
    _description_pattern = compile(r"^[a-zA-Z0-9\s]{0,255}")

    for i, entry in enumerate(work_experience):
        if i in (0, 1):
            _result = _validate_string_entry(entry, _company_job_pattern)
        elif i in (2, 3):
            _result = is_valid_date(entry)
        elif i == 4:
            _result = _validate_string_entry(entry, _description_pattern)
        else:
            raise ValueError("Unexpected index encountered during validation")

        if not _result["valid"]:
            return _return_exception(_result["message"])

    _start_date = datetime.strptime(work_experience[2], "%Y-%m-%d")
    _end_date = datetime.strptime(work_experience[3], "%Y-%m-%d")
    if _start_date >= _end_date:
        return _return_exception("The start date is unreasonable. Are you kidding?")

    return {"valid": True, "message": "The work experience is valid"}


def _validate_string_entry(entry: str, pattern) -> dict:
    if not isinstance(entry, str) or not pattern.match(entry):
        return _return_exception(f"The entered phrase ({entry}) is invalid\nPlease enter a phrase that is between "
                                 "5 and 30 characters long and only contains letters, numbers, and spaces")
    if _has_offensive_language(entry):
        return _return_exception(f"The phrase ({entry}) contains language that is considered offensive to some "
                                 f"people\nWe want to create a safe shopping environment for everyone\nOffensive "
                                 f"language can make people feel uncomfortable or unsafe")

    return {"valid": True, "message": "The phrase is valid"}


def _has_offensive_language(text: str) -> bool:
    _text_words = text.split(" ")
    for word in _text_words:
        if word.lower() in offensive_words:
            return True

    return False


def _return_exception(message: str) -> dict:
    return {"valid": False, "message": message}
