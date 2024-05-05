from phonenumbers import parse


def parse_phone_region(phone_number: str, region: str) -> int:
    return parse(phone_number, region).country_code
