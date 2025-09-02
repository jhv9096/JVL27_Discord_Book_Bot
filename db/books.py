from db.connection import get_connection, db_cursor

def insert_book(title, source, book_format, genre, tags, summary, url, added_by):
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

def update_book_field(book_id, field, value):
    allowed_fields = {"title", "source", "format", "genre", "tags", "summary", "url"}
    if field not in allowed_fields:
        raise ValueError(f"Field '{field}' is not editable.")

    with db_cursor() as cur:
        if field == "tags":
            cur.execute("UPDATE books SET tags = %s WHERE id = %s", ([value], book_id))
        else:
            cur.execute(f"UPDATE books SET {field} = %s WHERE id = %s", (value, book_id))