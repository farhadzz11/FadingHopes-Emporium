from database.MySQL.execute_command import execute_command


def delete_order(customer_id: str) -> dict:
    _result = execute_command("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))

    if not _result["execute"]:
        return {"delete": False, "message": _result["message"]}

    if len(_result["data"]) == 0:
        return {"delete": False, "message": "\nThere is nothing to delete"}

    while True:
        _order_id = input("\nPlease enter the order id you want to delete\n>>> ")

        _result = execute_command("SELECT * FROM orders WHERE orders_id = %s", (_order_id,))

        if not _result["execute"]:
            return {"delete": False, "message": _result["message"]}

        if len(_result["data"]) != 0:
            _product_id = _result["data"][0][2]
            _order_quantity = _result["data"][0][3]
            break
        else:
            print(f"\033[31m\nOrder id is not valid, Please enter a valid order id\033[0m")

    _result = execute_command("DELETE FROM orders WHERE orders_id = %s", (_order_id,))

    if not _result["execute"]:
        return {"delete": False, "message": _result["message"]}

    _result = execute_command(f"UPDATE product SET product_inventory = product_inventory + {_order_quantity} "
                              "WHERE product_id = %s",
                              [_product_id])

    if not _result["execute"]:
        return {"add": False, "message": _result["message"]}

    return {"delete": True, "message": f"{_order_id} successfully deleted"}
