import os
from mysql.connector import connect, Error


def connect_mysql() -> dict:
    try:
        # setx [variable name] [variable value]
        _username = os.getenv("DB_USERNAME")
        _password = os.getenv("DB_PASSWORD")
        _host = os.getenv("DB_HOST")
        _database = os.getenv("DB_NAME")

        _connection = connect(
            user=_username,
            password=_password,
            host=_host,
            database=_database
        )

        return {"connect": True, "data": _connection}

    except Error as e:
        return {"connect": False, "message": str(e)}
