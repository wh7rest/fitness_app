from db.database import get_connection


def seed_user():
    conn = get_connection()
    cur = conn.cursor()

    # проверяем, есть ли admin
    cur.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    existing = cur.fetchone()

    if existing:
        print("User already exists")
    else:
        cur.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """,
            ("admin", "123", "admin"),
        )

        conn.commit()
        print("Admin user created")

    conn.close()


if __name__ == "__main__":
    seed_user()
