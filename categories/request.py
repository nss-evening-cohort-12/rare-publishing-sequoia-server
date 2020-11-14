import sqlite3
import json

from models.category import Category

def create_category(new_category):
    with sqlite3.connect("./rare.db") as conn:
      db_cursor = conn.cursor()

      db_cursor.execute("""
      INSERT INTO categories
        ( name )
      VALUES
        (?)
      """, (new_category['name'], ))

      id = db_cursor.lastrowid

      new_category['id'] = id

    return json.dumps(new_category)

def get_all_categories():        
     with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            id,
            name
        FROM
            categories
        """)
        
        categories = []
        
        dataset = db_cursor.fetchall()

        for row in dataset:
            category = Category(row['name'], row['id'])
            
            categories.append(category.__dict__)

     return json.dumps(categories)      


def get_category_by_id(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            c.id,
            c.name
        FROM 
            categories c
        WHERE
            c.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        category = Category(data['name'], data['id'])

        return json.dumps(category.__dict__)

def update_category(id, new_category):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Categories
            SET
                name = ?
        WHERE id = ?
        """, (new_category['name'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True    

