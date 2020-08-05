import sqlite3


def create_connection(db_path):
    conn = sqlite3.connect(db_path)
    return conn


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    """Checks if a table exists.

    Args:
        conn: A db connection.
        table_name: The table to look for.

    Returns:
        A bool that indicates if the table exists.
    """

    query = f'''
    SELECT COUNT(name) FROM sqlite_master
    WHERE type='table' AND name='{table_name}';
    '''
    cursor = conn.cursor()
    cursor.execute(query)

    if cursor.fetchone()[0] == 1:
        return True
    return False
