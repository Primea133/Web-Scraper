import sqlite3
import csv

# Andmebaasi loomine
def init_db():
    conn = sqlite3.connect("amblik.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS andmed (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Price TEXT NOT NULL,
            Stock TEXT NOT NULL,
            image_href TEXT NOT NULL,
            groupID INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Loo andmebaas
init_db()