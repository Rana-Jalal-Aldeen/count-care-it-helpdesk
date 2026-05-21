import sqlite3

conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER,
    username TEXT,
    comment TEXT,
    created_at TEXT
)
""")

conn.commit()
conn.close()

print("Comments table created.")