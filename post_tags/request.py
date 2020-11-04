import sqlite3
import json


def tag_post(tag_details):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT OR IGNORE INTO post_tags
            (post_id, tag_id)
        VALUES
            (?, ?)
        """, (tag_details['post_id'], tag_details['tag_id']))

        id = db_cursor.lastrowid
        tag_details['id'] = id

        if tag_details['id'] > 0:
            is_valid = True
        else:
            is_valid = False

    return json.dumps({'valid': is_valid})
