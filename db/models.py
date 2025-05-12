### db/models.py

from db import get_connection, release_connection
from datetime import datetime
from typing import Optional
import logging

class User:
    def __init__(self, telegram_id: int, first_name: str, language_code: str):
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.language_code = language_code

    @staticmethod
    def get_or_create(telegram_id: int, first_name: str, language_code: str):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
                row = cur.fetchone()
                if not row:
                    cur.execute("INSERT INTO users (telegram_id,first_name,language_code) VALUES (%s,%s,%s)", (telegram_id,first_name,language_code,))
                    conn.commit()
        except Exception as e:
            logging.exception(f"❌ Exception in get_or_create_user: {e}")
        finally:
            release_connection(conn)  



def get_user_id_by_telegram_id(telegram_id: int) -> Optional[int]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
            row = cur.fetchone()
            return row["id"] if row else None
    except Exception as e:
        logging.exception(f"❌ Exception in get_or_create_user: {e}")
    finally:
        release_connection(conn) 

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
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO media_notes (name, author, category, status, user_id, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (self.name, self.author, self.category, self.status, self.user_id, self.created_at))
                conn.commit()
        except Exception as e:
            logging.exception(f"❌ Exception in get_or_create_user: {e}")
        finally:
            release_connection(conn)   

    @staticmethod
    def update_status(note_id: int, new_status: str):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE media_notes
                    SET status = %s
                    WHERE id = %s
                """, (new_status, note_id))
                conn.commit()
        except Exception as e:
            logging.exception(f"❌ Exception in get_or_create_user: {e}")
        finally:
            release_connection(conn)  
            
    @staticmethod
    def delete(note_id: int):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM media_notes WHERE id = %s", (note_id,))
                conn.commit()
        except Exception as e:
            logging.exception(f"❌ Exception in get_or_create_user: {e}")
        finally:
            release_connection(conn)         
