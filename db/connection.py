from contextlib import contextmanager
import psycopg2
import logging

def get_connection():
    # Your existing connection logic
    return psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="localhost",
        port="5432"
    )

@contextmanager
def db_cursor():
    conn = get_connection()
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Database error: {e}")
        raise
    finally:
        cur.close()
        conn.close()