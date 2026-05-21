import sqlite3

conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

# إضافة عمود status إذا ما كان موجود
try:
    cursor.execute("ALTER TABLE tickets ADD COLUMN status TEXT DEFAULT 'Offen'")
    print("Status column added!")
except:
    print("Column already exists.")

conn.commit()
conn.close()