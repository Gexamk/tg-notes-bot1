import psycopg2
import config
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(
        config.DATABASE_URL,
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