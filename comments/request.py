import sqlite3
import json

from models.comment import Comment
from models.User import User

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


def get_comments_by_post_id(post_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.subject,
            c.content,
            c.post_id,
            c.user_id,
            c.publication_date,
            u.id,
            u.first_name,
            u.last_name,
            u.display_name,
            u.email
        FROM comments c
        JOIN users u
            ON u.id = c.user_id
        WHERE c.post_id = ?
        ORDER BY c.publication_date DESC
        """, ( post_id, ))

        comments = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['subject'], row['content'], row['post_id'], row['user_id'], row['publication_date'])
            user = User(row['user_id'], row['first_name'], row['last_name'], row['email'], row['display_name'])

            comment.user = user.__dict__

            comments.append(comment.__dict__)

    return json.dumps(comments)
