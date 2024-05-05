from uuid import uuid4
from datetime import datetime
from database.MySQL.execute_command import execute_command
from entities.message import Message


def initial_setting(factor_id: str) -> dict:
    _result = execute_command("SELECT factor_paymentStatus FROM factor WHERE factor_id = %s",
                              (factor_id,))

    if not _result["execute"]:
        return {"initial_setting": False, "message": _result["message"]}

    _payment_status = _result["data"][0][0]

    if _payment_status != "paid":
        return {"initial_setting": False,
                "message": "The factor has not been paid yet\nPlease make sure it is paid first and then try "
                           f"again (payment status is {_payment_status})"}

    _result = execute_command("SELECT freight_status FROM freight WHERE factor_id = %s",
                              (factor_id,))

    if not _result["execute"]:
        return {"initial_setting": False, "message": _result["message"]}

    _freight_status = _result["data"][0][0]

    if _freight_status == "shipped":
        _message = Message()
        _message.id = str(uuid4())
        _result = execute_command("SELECT customer_id FROM factor WHERE factor_id = %s", (factor_id,))

        if not _result["execute"]:
            return {"initial_setting": False, "message": _result["message"]}

        _message.customer_id = _result["data"][0][0]
        _message.txt = f"Thanks for your purchase (ID -> {factor_id})"
        _message.date = str(datetime.now().date())
        _message.time = str(datetime.now().time().strftime("%H:%M:%S"))
        _message.seen = False

        _result = execute_command("INSERT INTO message VALUES(%s, %s, %s, %s, %s, %s)",
                                  [_message.id, _message.customer_id, _message.txt,
                                   _message.date, _message.time, _message.seen])

        if not _result["execute"]:
            return {"initial_setting": False, "message": _result["message"]}

        _result = execute_command("DELETE FROM orders WHERE customer_id = "
                                  "(SELECT customer_id FROM factor WHERE factor_id = %s)",
                                  (factor_id,))

        if not _result["execute"]:
            return {"initial_setting": False, "message": _result["message"]}

        return {"initial_setting": True, "message": "Orders have been successfully deleted"}
    else:
        return {"initial_setting": False, "message": "The products in the factor has not been shipped yet\n"
                                                     "Please make sure it is shipped "
                                                     f"first and then try again (freight status is {_freight_status})"}
