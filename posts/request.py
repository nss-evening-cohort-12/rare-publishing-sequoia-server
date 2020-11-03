import sqlite3
import json

from models.post import Post

def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO posts
            ( user_id, category_id, title, content, publication_date, header_img )
        VALUES
            (?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['content'], new_post['publication_date'], new_post['header_img'], ))

        id = db_cursor.lastrowid

        new_post['id'] = id

    return json.dumps(new_post)
