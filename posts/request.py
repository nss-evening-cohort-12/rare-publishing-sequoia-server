import sqlite3
import json

from models.post import Post
from models.User import User

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
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.content,
            p.publication_date,
            p.header_img,
            u.id,
            u.first_name,
            u.last_name,
            u.display_name,
            u.email
        FROM Posts p
        JOIN users u
            ON u.id = p.user_id
        ORDER BY p.publication_date DESC
        """)

        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['content'], row['publication_date'], row['header_img'])

            user = User(row['user_id'], row['first_name'], row['last_name'], row['email'], row['display_name'])

            post.user = user.__dict__

            posts.append(post.__dict__)
    
    return json.dumps(posts)


def get_posts_by_user(user_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.content,
            p.publication_date,
            p.header_img,
            u.id,
            u.first_name,
            u.last_name,
            u.display_name,
            u.email
        FROM Posts p
        JOIN users u
            ON u.id = p.user_id
        WHERE p.user_id = ?
        """, ( user_id, ))

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'], row['content'], row['publication_date'], row['header_img'])
            user = User(row['user_id'], row['first_name'], row['last_name'], row['email'], row['display_name'])

            post.user = user.__dict__
            
            posts.append(post.__dict__)

    return json.dumps(posts)

def get_post_by_id(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.content,
            p.publication_date,
            p.header_img,
            u.id,
            u.first_name,
            u.last_name,
            u.display_name,
            u.email
        FROM Posts p
        JOIN users u
            ON u.id = p.user_id
        WHERE p.id = ?
        """, (id , ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'], data['content'], data['publication_date'], data['header_img'])
        user = User(data['user_id'], data['first_name'], data['last_name'], data['email'], data['display_name'])

        post.user = user.__dict__
    
        return json.dumps(post.__dict__)

def delete_post(id):
    with sqlite3.connect('./rare.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, ( id, ))
