from re import compile
from string import punctuation
from data.regions import regions


def is_valid_price(price: str, region: str) -> dict:
    _price_pattern = compile(r"^\d+(\.\d+)?$")

    if not _price_pattern.match(price):
        return {"valid": False, "message": "Product name contains invalid characters\nProduct name may not contain "
                                           f"any of the following characters: {punctuation.split(".")}"}

    if not (0 < len(price) < 129):
        return {"valid": False,
                "message": "That price is a little out of this world\nLet's try a more realistic number"}

    if region not in regions:
        return {"valid": False,
                "message": "The region specified for the currency is invalid\nThe region must be one of the "
                           f"following: \n{regions}"}

    return {"valid": True, "message": "The price is valid"}
