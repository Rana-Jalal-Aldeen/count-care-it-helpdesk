import sqlite3

conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

cursor.execute("UPDATE tickets SET priority='Hoch' WHERE priority='High'")
cursor.execute("UPDATE tickets SET priority='Mittel' WHERE priority='Medium'")
cursor.execute("UPDATE tickets SET priority='Niedrig' WHERE priority='Low'")

conn.commit()
conn.close()

print("Alle Prioritäten wurden aktualisiert.")