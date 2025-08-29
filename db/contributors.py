from db.connection import get_connection

def insert_contributor(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO contributors (name) VALUES (%s) RETURNING id", (name,))
    contributor_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return contributor_id

def link_contributor_to_book(book_id, contributor_id, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO book_credits (book_id, contributor_id, role)
        VALUES (%s, %s, %s)
    """, (book_id, contributor_id, role))
    conn.commit()
    cur.close()
    conn.close()

def get_contributor_id_by_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM contributors WHERE name = %s", (name,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None