import sqlite3
import os

ACCOUNTS_TABLE_NAME = "Accounts"
DB_FILE_NAME = "accounts.db"


def make_query(query, values=None):

    module_dir = os.path.dirname(__file__)
    db_path = os.path.join(module_dir, DB_FILE_NAME)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    connection.commit()
    return cursor


def initialize_database():
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {ACCOUNTS_TABLE_NAME} (
        id INTEGER PRIMARY KEY,
        email_address TEXT NOT NULL,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        username TEXT NOT NULL,
        email_id TEXT NOT NULL
    )
    """
    make_query(create_table_query)


class AccountsTable:

    def __init__(self):
        self.account_index = 0

        try:
            self.get_all()
        except sqlite3.OperationalError:
            initialize_database()

    def add_one(self, email_address, name, password, username, email_id):
        query = f"INSERT INTO {ACCOUNTS_TABLE_NAME} (email_address, name, password, username, email_id) VALUES (?, ?, ?, ?, ?)"
        values = (email_address, name, password, username, email_id)
        result = make_query(query, values)
        return result

    def get_one_by_email(self, email_address):
        query = f"SELECT * FROM {ACCOUNTS_TABLE_NAME} WHERE email_address = ?"
        result = make_query(query, (email_address,)).fetchone()
        return result

    def get_random_account(self):
        query = f"SELECT * FROM {ACCOUNTS_TABLE_NAME} ORDER BY RANDOM() LIMIT 1"
        result = make_query(query).fetchone()
        return result

    def get_all(self):
        query = f"SELECT * FROM {ACCOUNTS_TABLE_NAME}"
        result = make_query(query).fetchall()
        return result

    def delete_one_by_email(self, email_address):
        query = f"DELETE FROM {ACCOUNTS_TABLE_NAME} WHERE email_address = ?"
        result = make_query(query, (email_address,))
        return result
