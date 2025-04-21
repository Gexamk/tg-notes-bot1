import psycopg2
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# Читаем данные
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Пробуем подключиться
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("Подключение к базе данных успешно!")

    # Можно открыть курсор и делать запросы
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("Версия PostgreSQL:", version)

    # Закрываем соединение
    cursor.close()
    conn.close()

except Exception as e:
    print("Ошибка подключения к базе:", e)