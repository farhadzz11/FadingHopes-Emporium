from uuid import uuid4
from database.MySQL.execute_command import execute_command
from entities.orders import Orders
from services.show_products import show_products


def add_order(customer_id: str) -> dict:
    try:
        _count_orders = int(input("\nHow many order you want to add?\n>>> "))
    except Exception as e:
        return {"add": False, "message": str(e)}

    if not (_count_orders > 0):
        return {"add": False, "message": "Invalid number, Enter a valid positive number for count"}

    show_products(customer_id)

    for i in range(_count_orders):
        order = Orders()
        order.id = str(uuid4())
        order.customer_id = customer_id

        while order.product_id == "null":
            order.product_id = input("\nPlease enter the product id you want to add\n>>> ")

        _result = execute_command("SELECT product_id FROM orders WHERE customer_id = %s",
                                  (customer_id,))

        if not _result["execute"]:
            return {"add": False, "message": _result["message"]}

        if _result["data"] == order.product_id:
            return {"add": False, "message": "\nThis product already is on your cart\n"
                                             "If you want to edit it, Please select edit the product in the list"}

        _result = execute_command("SELECT product_inventory FROM product WHERE product_id = %s",
                                  (order.product_id,))

        if _result["data"] == 0:
            return {"add": False, "message": "\nThis product is currently out of stock"
                                             "Please visit this product later\n"}

        while order.quantity == 0:
            order.quantity = int(input("\nHow many of this product do you want?\n>>> "))

        _total_price = order.calculate_price()

        _result = execute_command("INSERT INTO orders VALUES(%s, %s, %s, %s, %s)",
                                  [order.id, order.customer_id, order.product_id, order.quantity,
                                   _total_price["data"]])

        if not _result["execute"]:
            return {"add": False, "message": _result["message"]}

        _result = execute_command(f"UPDATE product SET product_inventory = product_inventory - {order.quantity} "
                                  "WHERE product_id = %s",
                                  [order.product_id])

        if not _result["execute"]:
            return {"add": False, "message": _result["message"]}

    return {"add": True, "message": f"Successfully added"}


if __name__ == "__main__":
    print(add_order('a227615d-be49-4471-bcee-dd6abed8c61c'))