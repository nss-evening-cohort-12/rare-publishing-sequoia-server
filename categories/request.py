import sqlite3
import json

from models.category import Category

def create_category(new_category):
    with sqlite3.connect("./rare.db") as conn:
      db_cursor = conn.cursor()

      db_cursor.execute("""
      INSERT INTO category
        ( )
      )
      
