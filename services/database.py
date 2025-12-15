import sqlite3

DB_NAME = "bot.db"


def init_db():
    with sqlite3.connect(DB_NAME) as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS filters (
            user_id INTEGER PRIMARY KEY,
            year INTEGER,
            rating REAL
        )
        """)
        db.commit()


def save_filters(user_id: int, year: int, rating: float):
    with sqlite3.connect(DB_NAME) as db:
        db.execute(
            "INSERT OR REPLACE INTO filters (user_id, year, rating) VALUES (?, ?, ?)",
            (user_id, year, rating)
        )
        db.commit()


def get_filters(user_id: int):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT year, rating FROM filters WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchone()

def reset_filters(user_id: int):
    with sqlite3.connect(DB_NAME) as db:
        db.execute("DELETE FROM filters WHERE user_id = ?", (user_id,))
        db.commit()
