import sqlite3
import json

from models import User


def create_user(new_user):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO users
            (first_name, last_name, email, display_name)
        VALUES
            (?, ?, ?, ?)
        """, (new_user['first_name'], new_user['last_name'], new_user['last_name'], new_user['first_name'] + ' ' + new_user['last_name']))

        id = db_cursor.lastrowid
        new_user['id'] = id

    return json.dumps(new_user)
