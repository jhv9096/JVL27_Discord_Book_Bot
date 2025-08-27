from db.connection import get_connection

def insert_user(discord_id, username, discriminator=None, nickname=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (discord_id, username, discriminator, nickname)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (discord_id) DO NOTHING
    """, (discord_id, username, discriminator, nickname))
    conn.commit()
    cur.close()
    conn.close()