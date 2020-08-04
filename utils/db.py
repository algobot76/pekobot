import sqlite3


def create_connection(db_path):
    conn = sqlite3.connect(db_path)
    return conn
