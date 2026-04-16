import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("realname.DB")


def init_db(TABLE_NAME) -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT NOT NULL UNIQUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        print(f"Database created: {DB_PATH}")
        print(f"Table ready: {TABLE_NAME}")
    finally:
        conn.close()


if __name__ == "__main__":
    init_db("test_phone_whitelist")
