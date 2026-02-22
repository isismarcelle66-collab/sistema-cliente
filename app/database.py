import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        email TEXT,
        telefone TEXT,
        status TEXT DEFAULT 'novo',
        user_id INTEGER REFERENCES users(id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()