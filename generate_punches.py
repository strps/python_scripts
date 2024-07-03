import sqlite3

connection = sqlite3.connect("db.db")
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS punch(
        punch_id INTEGER PRIMARY KEY,
        timestamp INTEGER,
        created_at INTEGER,
        user TEXT,
        flag TEXT,
        notes TEXT,   
        puch_date TEXT,
        punch_time TEXT,
        punch_timestamp INTEGER,
        notes TEXT
    );    
"""
)