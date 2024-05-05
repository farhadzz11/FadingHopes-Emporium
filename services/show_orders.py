from database.MySQL.execute_command import execute_command


def show_orders(customer_id: str) -> dict:
    _result = execute_command("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    _orders = _result["data"]

    print(f"\nThere are {len(_orders)} items in your cart")
    for row in _orders:
        print("----------------------------------------")
        print(f"Order ID = {row[0]}\n"
              f"Product ID             ->   {row[2]}\n"
              f"Quantity               ->   {row[3]}\n"
              f"Price                  ->   {row[4]}")

    return {"show": True, "message": "All products were displayed"}
