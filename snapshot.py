import os
import sqlite3
from datetime import datetime
from utils import compute_hash
from database import DB_FILE

def snapshot(directory):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO snapshots (timestamp) VALUES (?)", (datetime.now().isoformat(),))
    snapshot_id = cursor.lastrowid

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = compute_hash(file_path)

            cursor.execute("SELECT hash FROM file_data WHERE hash = ?", (file_hash,))
            if not cursor.fetchone():
                with open(file_path, 'rb') as f:
                    cursor.execute("INSERT INTO file_data (hash, content) VALUES (?, ?)", (file_hash, f.read()))

            cursor.execute("INSERT INTO files (snapshot_id, path, hash) VALUES (?, ?, ?)", (snapshot_id, file_path, file_hash))

    conn.commit()
    conn.close()
    print(f"Snapshot {snapshot_id} created.")
