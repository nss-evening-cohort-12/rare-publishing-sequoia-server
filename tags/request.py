import sqlite3
import json

#from models import Tag


def create_tag(new_tag):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT OR IGNORE INTO tags
            (name)
        VALUES
            (?)
        """, (new_tag['tag_name'],))

        id = db_cursor.lastrowid
        new_tag['id'] = id

        if new_tag['id'] > 0:
            is_valid = True
        else:
            is_valid = False

    return json.dumps({'valid': is_valid})
