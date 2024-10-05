import sqlite3
import os

TARGETS_TABLE_NAME = "Targets"
DB_FILE_NAME = "targets.db"


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
    CREATE TABLE IF NOT EXISTS {TARGETS_TABLE_NAME} (
        id INTEGER PRIMARY KEY,
        tweet_id INT,
        action_type VARCHAR(10),
        target_username VARCHAR(256),
        target_tweet_id VARCHAR(256),
        target_page_name VARCHAR(256)
    )
    """
    make_query(create_table_query)


class TargetsTable:

    def __init__(self):
        self.current_target_index = 0

        try:
            self.get_all()
        except sqlite3.OperationalError:
            initialize_database()

    def add_one(self, tweet_id, action_type, target_username, target_tweet_id):
        query = f"INSERT INTO {TARGETS_TABLE_NAME} (tweet_id, action_type, target_username, target_tweet_id) VALUES (?, ?, ?, ?)"
        values = (tweet_id, action_type, target_username, target_tweet_id)
        result = make_query(query, values)
        return result

    def get_all(self):
        query = f"SELECT * FROM {TARGETS_TABLE_NAME}"
        result = make_query(query).fetchall()
        return result

    def get_one_retweet(self, target_tweet_id):
        query = f"SELECT * FROM {TARGETS_TABLE_NAME} WHERE target_tweet_id = ?"
        result = make_query(query, (target_tweet_id,)).fetchone()
        return result

    def get_all_with_same_tweet_id(self, tweet_id):
        query = f"SELECT * FROM {TARGETS_TABLE_NAME} WHERE tweet_id = ?"
        result = make_query(query, (tweet_id,)).fetchall()
        return result

    def get_all_with_same_page(self, page_name):
        query = f"SELECT * FROM {TARGETS_TABLE_NAME} WHERE target_page_name = ?"
        result = make_query(query, (page_name,)).fetchall()
        return result

    def get_all_with_same_action_type(self, action_name):
        query = f"SELECT * FROM {TARGETS_TABLE_NAME} WHERE action_name = ?"
        result = make_query(query, (action_name,)).fetchall()
        return result

    def delete_all_with_same_tweet_id(self, tweet_id):
        query = f"DELETE FROM {TARGETS_TABLE_NAME} WHERE tweet_id = ?"
        result = make_query(query, (tweet_id,)).fetchall()
        return result

    def delete_all_with_same_page(self, page_name):
        query = f"DELETE FROM {TARGETS_TABLE_NAME} WHERE target_page_name = ?"
        result = make_query(query, (page_name,)).fetchall()
        return result

    def get_all_with_same_tweet_id_and_action_type(self, tweet_id, action_name):
        query = f"SELECT * FROM {TARGETS_TABLE_NAME} WHERE tweet_id = ? and action_type = ?"
        result = make_query(query, (tweet_id, action_name)).fetchall()
        return result

    def get_all_with_same_tweet_id_and_page_name(self, tweet_id, page_name):
        query = f"SELECT * FROM {TARGETS_TABLE_NAME} WHERE tweet_id = ? and page_name = ?"
        result = make_query(query, (tweet_id, page_name)).fetchall()
        return result

    def get_all_with_same_action_type_and_page_name(self, action_name, page_name):
        query = f"SELECT * FROM {TARGETS_TABLE_NAME} WHERE action_type = ? and page_name = ?"
        result = make_query(query, (action_name, page_name)).fetchall()
        return result
