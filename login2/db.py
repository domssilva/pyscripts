import sqlite3
import logging
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv('DB_NAME')

# creates file if it doesn't exist / if it exists, creates connection
def db_connect():
    try:
        connection = sqlite3.connect(DB_NAME)
        # cursor is used to execute SQL queries
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        logging.error('Could not create DB connection')

def init_users_table():
    conn, cur = db_connect()
try:
    # create users table
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
           );""")
        # commit transaction
        conn.commit()
        # close existing connection
        conn.close()
        logging.info('Table users succesfully created.')
except Exception as e:
    logging.error('Could not initialize users table')

def create_user(username, password):
    conn, cur = db_connect()
    try:
        # WIP
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, password)
        logging.info(f'New user {username} created')
    except Exception as e:
        logging.error(f'Could not create user {username}')



