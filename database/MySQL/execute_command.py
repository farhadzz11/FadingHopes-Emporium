from mysql.connector import Error
from database.MySQL.connect_mysql import connect_mysql


def execute_command(command: str, params) -> dict:
    if params is None:
        params = []
    _result = connect_mysql()

    if not _result["connect"]:
        return {"execute": False, "message": _result["message"]}

    _connection = _result["data"]
    _cursor = None
    try:
        _cursor = _connection.cursor()
        _cursor.execute(command, params)

        if command.strip().upper().startswith('SELECT'):
            _data = _cursor.fetchall()

            return {"execute": True, "data": _data}
        else:
            _connection.commit()

            return {"execute": True, "message": "Command executed successfully"}
    except Error as e:
        return {"execute": False, "message": str(e)}
    finally:
        if _cursor is not None:
            _cursor.close()
        if _connection.is_connected():
            _connection.close()
