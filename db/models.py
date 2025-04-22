from dataclasses import dataclass
from datetime import datetime   
from typing import Optional


class MediaNote:
    def __init__(self, name: str, author: Optional[str], category: str, status: str, user_id: int, id: Optional[int] = None, created_at: Optional[str] = None):
        self.id = id
        self.name = name
        self.author = author
        self.category = category
        self.status = status
        self.user_id = user_id
        self.created_at = created_at

    def save(self, db) -> int:
        query = """
            INSERT INTO media_notes (name, author, category, status, user_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """
        with db.conn.cursor() as cur:
            cur.execute(query, (self.name, self.author, self.category, self.status, self.user_id))
            self.id = cur.fetchone()[0]
            db.conn.commit()
            return self.id
        
@dataclass
class User:
    id: int
    telegram_id: int