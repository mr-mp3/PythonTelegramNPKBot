import sqlite3
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_name='requests.db'):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    request_text TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Ошибка создания таблицы: {e}")

    def save_request(self, user_id, username, request_text):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO user_requests (user_id, username, request_text) VALUES (?, ?, ?)',
                (user_id, username, request_text)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения в БД: {e}")
            return False