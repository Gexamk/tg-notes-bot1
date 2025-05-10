import psycopg2
import config
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG
import os
from dotenv import load_dotenv
from psycopg2 import OperationalError, InterfaceError

DB_POOL = pool.SimpleConnectionPool(
    1, 10,  # minconn, maxconn
    dsn=os.getenv("DATABASE_URL"),
    cursor_factory=RealDictCursor
)


#def get_connection():
#    return DB_POOL.getconn()

def get_connection():
    conn = DB_POOL.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
        return conn
    except (OperationalError, InterfaceError):
        try:
            conn.close()  # полностью убираем битое соединение
        except Exception:
            pass
        return DB_POOL.getconn()  # берём новое

def release_connection(conn):
    if conn:
        DB_POOL.putconn(conn)


def get_connection_URL():
    return psycopg2.connect(
        os.getenv("DATABASE_URL"),
        cursor_factory=RealDictCursor
    )


def get_connection_local():
    return psycopg2.connect(
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        cursor_factory=RealDictCursor
    )