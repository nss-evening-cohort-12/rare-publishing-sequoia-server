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


def get_all_posts():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor

        db_cursor.execute("""
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.content,
            p.publication_date,
            p.header_img
        FROM Posts p
        """)

        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['content'], row['publication_date'], row['header_img'])

            posts.append(post.__dict__)
    
    return json.dumps(posts)
