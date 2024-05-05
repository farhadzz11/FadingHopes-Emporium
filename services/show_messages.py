from database.MySQL.execute_command import execute_command


def show_messages(customer_id: str, seen: bool) -> dict:
    if seen:
        _result = execute_command("SELECT * FROM message "
                                  "WHERE customer_id = %s AND message_seen = False "
                                  "ORDER BY message_date DESC, message_time DESC",
                                  (customer_id,))

        if len(_result["data"]) == 0:
            return {"show": False, "message": "All messages have been viewed"}
    else:
        _result = execute_command("SELECT * FROM message "
                                  "WHERE customer_id = %s "
                                  "ORDER BY message_date DESC, message_time DESC",
                                  (customer_id,))

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    for message_info in _result["data"]:
        print("---------------------------------------\n"
              f"message id            ->   {message_info[0]}\n"
              f"message text          ->   {message_info[2]}\n"
              f"message date          ->   {message_info[3]}\n"
              f"message time          ->   {message_info[4]}")

    _result = execute_command("UPDATE message SET message_seen = True "
                              "WHERE customer_id = %s "
                              "ORDER BY message_date DESC, message_time DESC",
                              (customer_id,))

    if not _result["execute"]:
        return {"show": False, "message": _result["message"]}

    return {"show": True, "message": "It was successfully shown"}
