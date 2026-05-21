import sqlite3

conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE tickets ADD COLUMN priority TEXT DEFAULT 'Medium'")
    print("Priority column added!")
except:
    print("Priority column already exists.")

conn.commit()
conn.close()