from db.connection import get_connection

def insert_book(title, source, format, genre, tags, summary, url, added_by):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO books (title, source, format, genre, tags, summary, url, added_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (title, source, format, genre, tags, summary, url, added_by))
    conn.commit()
    cur.close()
    conn.close()