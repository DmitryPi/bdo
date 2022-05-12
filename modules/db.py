import sqlite3
import logging

from modules.utils import load_config, handle_error


class Database:
    def __init__(self):
        self.config = load_config()
        self.sql_create_main_table = """
            CREATE TABLE IF NOT EXISTS {} (
                id integer PRIMARY KEY,
                proj_id integer NOT NULL UNIQUE,
                url text NOT NULL,
                title text NOT NULL,
                body text NOT NULL,
                budget text NOT NULL,
                deadline text NOT NULL,
                sent boolean NOT NULL,
                created text NOT NULL
            );""".format(self.config['DB']['table'])
        self.sql_insert_main = """
            INSERT OR IGNORE INTO {} (
                    proj_id,
                    url,
                    title,
                    body,
                    budget,
                    deadline,
                    sent,
                    created
                )
                VALUES(?,?,?,?,?,?,?,?)
            """.format(self.config['DB']['table'])

    def db_create_connection(self, db_file='db.sqlite3'):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            logging.info(f'- Connected to db\n')
        except Exception as e:
            handle_error(e)
        return conn

    def db_create_table(self, conn, sql):
        try:
            cur = conn.cursor()
            cur.execute(sql)
        except Exception as e:
            handle_error(e)

    def db_create_tables(self, conn):
        try:
            self.db_create_table(conn, self.sql_create_main_table)
        except Exception as e:
            handle_error(e)

    def db_insert_object(self, conn, sql, data):
        try:
            cur = conn.cursor()
            cur.execute(sql, data)
            conn.commit()
        except Exception as e:
            handle_error(e)

    def db_get_all_objects(self, conn, table):
        try:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {table}')
            return cur.fetchall()
        except Exception as e:
            handle_error(e)

    def db_get_all_objects_filter(self, conn, table, column, value):
        try:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM {table} WHERE {column}=?', (value,))
            return cur.fetchall()
        except Exception as e:
            handle_error(e)

    def db_update_object(self, conn, table, column, idd, data):
        cur = conn.cursor()
        cur.execute(f'UPDATE {table} SET {column}=? WHERE {idd}=?', data)
        conn.commit()

    def db_get_all_field_values(self, conn, field, table):
        try:
            conn.row_factory = lambda cursor, row: row[0]
            cur = conn.cursor()
            ids = cur.execute(f'SELECT {field} FROM {table}').fetchall()
            return ids
        except Exception as e:
            handle_error(e)

    def db_insert_project(self, conn, data):
        try:
            with conn:
                self.db_insert_object(conn, self.sql_insert_main, data)
        except Exception as e:
            handle_error(e)
