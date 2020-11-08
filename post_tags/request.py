import sqlite3
import json

from models import PostTag, Tag


def remove_post_tag(post_tag_id):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM 
            post_tags
        WHERE
            id = ?
        """, (post_tag_id,))


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


def get_all_post_tags():
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id,
            t.name
        FROM
            post_tags pt
        JOIN
            tags t
        ON
            pt.tag_id = t.id
        """)

        post_tags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post_tag = PostTag(row['id'], row['post_id'], row['tag_id'])

            tag = Tag(row['tag_id'], row['name'])
            post_tag.tag = tag.__dict__

            post_tags.append(post_tag.__dict__)

    return json.dumps(post_tags)


def get_post_tags_by_post_id(post_id):
    with sqlite3.connect('./rare.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            pt.id,
            pt.post_id,
            pt.tag_id,
            t.name
        FROM
            post_tags pt
        JOIN
            tags t
        ON
            pt.tag_id = t.id
        WHERE
            pt.post_id = ?
        """, (post_id,))

        post_tags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post_tag = PostTag(row['id'], row['post_id'], row['tag_id'])

            tag = Tag(row['tag_id'], row['name'])
            post_tag.tag = tag.__dict__

            post_tags.append(post_tag.__dict__)

    return json.dumps(post_tags)
