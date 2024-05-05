from uuid import uuid4
from datetime import datetime
from database.MySQL.execute_command import execute_command
from entities.factor import Factor
from entities.freight import Freight
from services.show_orders import show_orders


def checkout(customer_id: str) -> dict:
    _result = execute_command("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))

    if not _result["execute"]:
        return {"checkout": False, "message": _result["message"]}

    if len(_result["data"]) == 0:
        return {"checkout": False, "message": "There are no orders to checkout"}

    _available_driver = False
    _result = execute_command("SELECT * FROM driver", None)

    if not _result["execute"]:
        return {"checkout": False, "message": _result["message"]}

    _drivers_information = _result["data"]
    _driver_id = ""
    for driver in _drivers_information:
        if driver[2]:
            _driver_id = driver[0]
            _result = execute_command("UPDATE driver SET driver_availableForFreight = False WHERE employee_id = %s",
                                      (_driver_id,))

            if not _result["execute"]:
                return {"checkout": False, "message": _result["message"]}
            _available_driver = True

    if not _available_driver:
        return {"checkout": False, "message": "Unfortunately, There are no drivers available to deliver your orders "
                                              "at this time\nPlease try again later"}

    _factor = Factor()
    _factor.id = str(uuid4())
    _factor.customer_id = customer_id
    _total_price = _factor.calculate_total_price()

    if not _total_price["calculate"]:
        return {"checkout": False, "message": _total_price["message"]}

    _factor.date = str(datetime.now().date())
    _factor.time = str(datetime.now().time().strftime("%H:%M:%S"))

    _result = show_orders(customer_id)

    if not _result["show"]:
        return {"checkout": False, "message": _result["message"]}

    print(f"\nTotal price -> {_total_price["data"]}\n")

    print("\nredirect to bank payment page . . .")
    # Payment process
    print("payment successfully\n")
    _factor.payment_status = "paid"

    _result = execute_command("INSERT INTO factor VALUES(%s, %s, %s, %s, %s, %s)",
                              [_factor.id, _factor.customer_id, _total_price["data"], _factor.payment_status,
                               _factor.date, _factor.time])

    if not _result["execute"]:
        return {"checkout": False, "message": _result["message"]}

    _freight = Freight()
    _freight.id = str(uuid4())
    _freight.factor_id = _factor.id
    _freight.driver_id = _driver_id
    _freight.status = "loading"

    _result = execute_command("INSERT INTO freight VALUES(%s, %s, %s, NULL, NULL, %s)",
                              [_freight.id, _freight.factor_id, _freight.driver_id, _freight.status])

    if not _result["execute"]:
        return {"checkout": False, "message": _result["message"]}

    _result = execute_command("SELECT freight_status FROM freight WHERE freight_id = %s", (_freight.id,))

    if not _result["execute"]:
        return {"checkout": False, "message": _result["message"]}

    print(f"\nThe shipping status of your orders status: {_result["data"][0][0]}")

    return {"checkout": True, "message": f"{_freight.id} successfully added"}
