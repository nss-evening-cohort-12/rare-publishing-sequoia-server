import sqlite3
import json

from models import User


def register_user(new_user):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT OR IGNORE INTO users
            (first_name, last_name, email, display_name)
        VALUES
            (?, ?, ?, ?)
        """, (new_user['first_name'], new_user['last_name'], new_user['last_name'], new_user['first_name'] + ' ' + new_user['last_name']))

        id = db_cursor.lastrowid
        new_user['id'] = id

        if new_user['id'] > 0:
            is_valid = True
        else:
            is_valid = False

    # return json.dumps(new_user)
    return json.dumps({'valid': is_valid, 'token': new_user['id']})
