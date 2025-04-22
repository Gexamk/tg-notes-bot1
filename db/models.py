### db/models.py

from db import get_connection
from datetime import datetime


class User:
    def __init__(self, telegram_id: int):
        self.telegram_id = telegram_id

    @staticmethod
    def get_or_create(telegram_id: int):
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
            row = cur.fetchone()
            if not row:
                cur.execute("INSERT INTO users (telegram_id) VALUES (%s)", (telegram_id,))
                conn.commit()


class MediaNote:
    def __init__(self, name, author, category, status, user_id):
        self.name = name
        self.author = author
        self.category = category
        self.status = status
        self.user_id = user_id
        self.created_at = datetime.utcnow()

    def save(self):
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO media_notes (name, author, category, status, user_id, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (self.name, self.author, self.category, self.status, self.user_id, self.created_at))
            conn.commit()
