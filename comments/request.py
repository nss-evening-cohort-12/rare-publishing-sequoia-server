import sqlite3
import json

from models.comment import Comment

def create_comment(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO comments
            ( subject, content, post_id, user_id, publication_date )
        VALUES
            (?, ?, ?, ?, ?);
        """, (new_comment['subject'], new_comment['content'], new_comment['post_id'], new_comment['user_id'], new_comment['publication_date'], ))

        id = db_cursor.lastrowid

        new_comment['id'] = id

    return json.dumps(new_comment)
