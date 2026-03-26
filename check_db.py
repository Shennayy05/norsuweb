import sqlite3
import os

db_path = 'db.sqlite3'
if not os.path.exists(db_path):
    print(f"Database file {db_path} not found.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dashboard_academiccalendar';")
    result = cursor.fetchone()
    if result:
        print("Table dashboard_academiccalendar EXISTS.")
    else:
        print("Table dashboard_academiccalendar DOES NOT exist.")
    conn.close()
