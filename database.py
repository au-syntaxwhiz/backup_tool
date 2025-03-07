import sqlite3

DB_FILE = "backup.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER,
            path TEXT NOT NULL,
            hash TEXT NOT NULL,
            FOREIGN KEY(snapshot_id) REFERENCES snapshots(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_data (
            hash TEXT PRIMARY KEY,
            content BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
