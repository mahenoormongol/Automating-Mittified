import sqlite3
import os

db_path = os.path.join("data", "mittified.db")
if not os.path.exists(db_path):
    print("Database not found at", db_path)
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Analyses Table Columns ---")
cursor.execute("PRAGMA table_info(analyses)")
cols = cursor.fetchall()
col_names = [c[1] for c in cols]
print("Columns:", col_names)

conn.close()

