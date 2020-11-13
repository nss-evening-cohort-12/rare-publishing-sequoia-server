import sqlite3
import json

from models import Tag


def update_tag(tag_id, post_body):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE tags
        SET
            name = ?
        WHERE
            id = ?
        """, (post_body['name'], tag_id))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


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


def get_tag_by_id(tag_id):
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM
            tags t
        WHERE
            id = ?
        """, (tag_id,))

        data = db_cursor.fetchone()

        post = Tag(data['id'], data['name'])

        return json.dumps(post.__dict__)

    return json.dumps(post_tags)
