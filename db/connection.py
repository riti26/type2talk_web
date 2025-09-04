import sqlite3
import os
from config import DB_FOLDER, DB_PATH

if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")  # 🔹 important!
    return conn