import sqlite3 as sq
import os


def create_table():
    with sq.connect(os.path.join('database', 'data_base.db')) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS query(
        id_query INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_user_id INTEGER,
        command TEXT,
        time INTEGER,
        urls TEXT
        )""")
    print('Data base connected OK!')


async def insert_into_query(data: dict):
    with sq.connect(os.path.join('database', 'data_base.db')) as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO query VALUES (NULL, ?, ?, ?, ?)",
            (data['tg_user_id'], data['command'], data['query_time'], ' | '.join(data['urls']))
        )


async def select_from_query(tg_user_id: int) -> list[tuple]:
    with sq.connect(os.path.join('database', 'data_base.db')) as con:
        cur = con.cursor()
        query_list: list[tuple] = cur.execute(
            f"""SELECT command, time, urls
            FROM query
            WHERE tg_user_id = {tg_user_id}"""
        ).fetchall()
    return query_list