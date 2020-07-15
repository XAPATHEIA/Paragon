import sqlite3
from sqlite3 import Error


# function to establish database connection
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB was successful.")
    except Error as e:
        print(f"The error '{e}' occurred.")

    return connection
