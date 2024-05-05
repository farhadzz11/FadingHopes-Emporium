from data.currency_units import currency_units
from database.MySQL.execute_command import execute_command


def get_currency_conversion_rate(customer_region: str, salesperson_region: str) -> float:
    _conversion_rates = {
        "US": {"AU": 0.6536, "IR": 0.00002, "GB": 1.25889, "CN": 0.13947, "JP": 0.00679, "CA": 0.73649, "KR": 0.00076,
               "MX": 0.05773, "IN": 0.012},
        "AU": {"US": 1.52114, "IR": 0.00004, "GB": 1.91494, "CN": 0.21216, "JP": 0.01033, "CA": 1.1203, "KR": 0.00116,
               "MX": 0.08782, "IN": 0.01825},
        "IR": {"US": 41994.2, "AU": 27578.68, "GB": 52864.83, "CN": 5878.46, "JP": 289.05, "CA": 30964.53, "KR": 31.85,
               "MX": 2427.73, "IN": 504.71},
        "GB": {"US": 0.79479, "AU": 0.52165, "IR": 0.00001, "CN": 0.11106, "JP": 0.00546, "CA": 0.5849, "KR": 0.0006,
               "MX": 0.04587, "IN": 0.00953},
        "CN": {"US": 7.15666, "AU": 4.6973, "IR": 0.00017, "GB": 9.00552, "JP": 0.04926, "CA": 5.26514, "KR": 0.00541,
               "MX": 0.41303, "IN": 0.08588},
        "JP": {"US": 145.18617, "AU": 95.25934, "IR": 0.00345, "GB": 182.55375, "CN": 20.28293, "CA": 106.77242,
               "KR": 0.10996, "MX": 8.37098, "IN": 1.74177},
        "CA": {"US": 1.35977, "AU": 0.89168, "IR": 0.00003, "GB": 1.70929, "CN": 0.19001, "JP": 0.00935, "KR": 0.00102,
               "MX": 0.07834, "IN": 0.01631},
        "KR": {"US": 1321.06, "AU": 866.27877, "IR": 0.03143, "GB": 1660.29, "CN": 184.53932, "JP": 9.08487,
               "CA": 971.3999, "MX": 76.16969, "IN": 15.84756},
        "EUR": {"US": 0.92715, "DE": 1.00, "AU": 0.60944, "IT": 1.00, "IR": 0.00002, "GB": 1.16724, "CN": 0.12931,
                "FR": 1.00, "JP": 0.0063, "CA": 0.68283, "KR": 0.0007, "MX": 0.05353, "IN": 0.01112, "ES": 1.00}
    }

    if customer_region in ["DE", "IT", "FR", "ES"]:
        return _conversion_rates["EUR"][salesperson_region]
    else:
        return _conversion_rates[customer_region][salesperson_region]


def convert_product_price(product_price: float, currency_conversion_rate: float, customer_id: str) -> dict:
    _converted_price = product_price * currency_conversion_rate

    _converted_price = round(_converted_price, 3)

    _result = execute_command("SELECT person.person_region FROM person INNER JOIN customer ON "
                              "person.person_id = customer.person_id "
                              "WHERE person.person_id = %s",
                              (customer_id,))

    if not _result["execute"]:
        return {"calculate": False, "message": _result["message"]}

    _customer_region = _result["data"][0][0]

    return {"convert": True, "data": f"{currency_units[_customer_region]}{_converted_price}"}
