from db.connection import get_connection

def insert_book(title, source, book_format, genre, tags, summary, url, added_by):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO books (title, source, format, genre, tags, summary, url, added_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (title, source, book_format, genre, tags, summary, url, added_by))
    conn.commit()
    cur.close()
    conn.close()

def get_book_summaries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            b.id,
            b.title,
            b.format,
            b.source,
            b.has_contributors,
            bc.role,
            c.name
        FROM books b
        LEFT JOIN book_credits bc ON b.id = bc.book_id
        LEFT JOIN contributors c ON bc.contributor_id = c.id
        ORDER BY b.added_at DESC;
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def get_all_books():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT title, format, source
        FROM books
        ORDER BY added_at DESC;
    """)
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books