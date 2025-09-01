from db.connection import get_connection, db_cursor

def insert_book(title, source, book_format, genre, tags, summary, url, added_by):
    # conn = get_connection()
    # cur = conn.cursor()
    with db_cursor() as cur:
        cur.execute("""
                INSERT INTO books (title, source, format, genre, tags, summary, url, added_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (title, source, book_format, genre, tags, summary, url, added_by))

def get_book_summaries():
    with db_cursor() as cur:
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
        return cur.fetchall()

# def get_book_summaries():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT
#             b.id,
#             b.title,
#             b.format,
#             b.source,
#             b.has_contributors,
#             bc.role,
#             c.name
#         FROM books b
#         LEFT JOIN book_credits bc ON b.id = bc.book_id
#         LEFT JOIN contributors c ON bc.contributor_id = c.id
#         ORDER BY b.added_at DESC;
#     """)
#     results = cur.fetchall()
#     cur.close()
#     conn.close()
#     return results

def get_all_books():
    with db_cursor() as cur:
        cur.execute("""
            SELECT title, format, source
            FROM books
            ORDER BY added_at DESC;
        """)
        return cur.fetchall()

def book_exists(book_id):
    with db_cursor() as cur:
        cur.execute("SELECT 1 FROM books WHERE id = %s", (book_id,))
        return cur.fetchone() is not None

def get_book_id_by_title(title):
    with db_cursor() as cur:
        cur.execute("SELECT id FROM books WHERE title = %s", (title,))
        result = cur.fetchone()
        return result[0] if result else None

# def get_all_books():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT title, format, source
#         FROM books
#         ORDER BY added_at DESC;
#     """)
#     books = cur.fetchall()
#     cur.close()
#     conn.close()
#     return books
#
# def book_exists(book_id):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT 1 FROM books WHERE id = %s", (book_id,))
#     exists = cur.fetchone() is not None
#     cur.close()
#     conn.close()
#     return exists
#
# def get_book_id_by_title(title):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT id FROM books WHERE title = %s", (title,))
#     result = cur.fetchone()
#     cur.close()
#     conn.close()
#     return result[0] if result else None