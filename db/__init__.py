import psycopg2
import config
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG
import os
from dotenv import load_dotenv


DB_POOL = pool.SimpleConnectionPool(
    1, 10,  # minconn, maxconn
    dsn=os.getenv("DATABASE_URL"),
    cursor_factory=RealDictCursor
)


def get_connection():
    return DB_POOL.getconn()

def release_connection(conn):
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