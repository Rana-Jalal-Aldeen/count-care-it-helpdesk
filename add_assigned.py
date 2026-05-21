import sqlite3

conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE tickets ADD COLUMN assigned_to TEXT DEFAULT 'Nicht zugewiesen'")
    print("Assigned column added!")
except:
    print("Assigned column already exists.")

conn.commit()
conn.close()