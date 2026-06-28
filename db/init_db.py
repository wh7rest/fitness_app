import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "app.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def create_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)

    connection.commit()
    connection.close()
    print("База данных создана!")

if __name__ == "__main__":
    create_database()
