import os
import sqlite3
from database import DB_FILE

def restore(snapshot_id, restore_directory):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT path, hash FROM files WHERE snapshot_id = ?", (snapshot_id,))
    files = cursor.fetchall()

    if not files:
        print("No snapshot found.")
        return

    os.makedirs(restore_directory, exist_ok=True)

    for file_path, file_hash in files:
        cursor.execute("SELECT content FROM file_data WHERE hash = ?", (file_hash,))
        file_data = cursor.fetchone()
        if file_data:
            restore_path = os.path.join(restore_directory, os.path.relpath(file_path))
            os.makedirs(os.path.dirname(restore_path), exist_ok=True)
            with open(restore_path, 'wb') as f:
                f.write(file_data[0])

    conn.close()
    print(f"Snapshot {snapshot_id} restored to {restore_directory}.")
