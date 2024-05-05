from database.MySQL.execute_command import execute_command


def login_process(username: str, password: str, access_level: str) -> dict:
    if access_level.lower() not in ("user", "admin"):
        return {"login": False,
                "message": "Invalid access level. Valid values are \"user\" and \"admin\""}

    if access_level == "user":
        _result = execute_command("SELECT person_id FROM customer "
                                  f"WHERE customer.customer_username = %s AND customer.customer_password = %s",
                                  [username, password])

    else:
        _result = execute_command("SELECT admin_id FROM admins "
                                  "WHERE admins.admin_username = %s AND admins.admin_password = %s",
                                  [username, password])

    if not _result["execute"]:
        return {"login": False, "message": _result["message"]}

    if len(_result["data"]) == 0:
        return {"login": False,
                "message": "Invalid username or password\nPlease enter a correct username or password"}

    if access_level == "user":
        return {"login": True,
                "data": _result["data"],
                "access_level": "user"}
    else:
        return {"login": True,
                "data": _result["data"],
                "access_level": "admin"}
