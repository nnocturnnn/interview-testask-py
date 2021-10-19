import os

import psycopg2
from psycopg2.extras import DictCursor

from config import DATABASE_URL


def init_database() -> None:
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        id BIGINT UNIQUE,
                        time TIMESTAMP,
                        data TEXT);
                        """)
            conn.commit()


def add_user(user_id: str) -> None:
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO users VALUES(%s, %s, %s)
                        ON CONFLICT (id) DO NOTHING;""",(user_id, "", ""))
            conn.commit()

 
def append_last_request(user_id: str, data: str, time) -> None:
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            sql = """UPDATE users SET data = %s, time = %s WHERE id= %s"""
            cur.execute(sql, (data, time, user_id))
            conn.commit()


def get_user(user_id: str) -> dict:
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""SELECT * FROM users WHERE id = %s""", (user_id))
            return cur.fetchone()


