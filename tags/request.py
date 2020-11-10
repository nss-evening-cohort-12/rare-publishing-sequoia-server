import sqlite3
import json

from models import Tag


def delete_tag(tag_id):
    with sqlite3.connect('./rare.db') as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM
            tags
        WHERE
            id = ? 
        """, (tag_id,))


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


def get_all_tags():
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            id,
            name
        FROM
            tags
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['name'])

            tags.append(tag.__dict__)

    return json.dumps(tags)
