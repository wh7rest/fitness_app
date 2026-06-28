import sqlite3
import os

def get_connection():
    db_dir = os.path.abspath("assets")
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    db_path = os.path.join(db_dir, "app.db")
    conn = sqlite3.connect(db_path)
    # Позволяет считывать строки как словари и как кортежи одновременно
    conn.row_factory = sqlite3.Row 
    return conn