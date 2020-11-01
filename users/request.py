import sqlite3
import json

from models import User


def register_user(new_user):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        # INSERT OR IGNORE - if the entry would not satisfy the UNIQUE constraint
        # (i.e. the email is not unique in the database) We just ignore the insert.
        #
        # When we do this, the `lastrowid` result is 0, instead of a positive,
        # non-zero integer, and therefore we can check if the insert was "valid" or not.

        db_cursor.execute("""
        INSERT OR IGNORE INTO users
            (first_name, last_name, email, display_name)
        VALUES
            (?, ?, ?, ?)
        """, (new_user['first_name'], new_user['last_name'], new_user['email'],
              new_user['first_name'] + ' ' + new_user['last_name']))

        id = db_cursor.lastrowid
        new_user['id'] = id

        if new_user['id'] > 0:
            is_valid = True
            token = new_user['id']
        else:
            is_valid = False
            token = ''

    return json.dumps({'valid': is_valid, 'token': token})


def login_user(login_details):
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            id,
            email
        FROM users
        WHERE email = ?
        """, (login_details['username'],))

        user = db_cursor.fetchall()

        if user:
            is_valid = True
            token = user[0]['id']
        else:
            is_valid = False
            token = ''

    return json.dumps({'valid': is_valid, 'token': token})
