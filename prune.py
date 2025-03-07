import sqlite3
from database import DB_FILE

def prune(keep_last):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM snapshots ORDER BY timestamp DESC LIMIT ? OFFSET ?", (keep_last, keep_last))
    snapshots_to_delete = cursor.fetchall()

    for (snapshot_id,) in snapshots_to_delete:
        cursor.execute("DELETE FROM files WHERE snapshot_id = ?", (snapshot_id,))
        cursor.execute("DELETE FROM snapshots WHERE id = ?", (snapshot_id,))

    cursor.execute("DELETE FROM file_data WHERE hash NOT IN (SELECT DISTINCT hash FROM files)")

    conn.commit()
    conn.close()
    print(f"Pruned old snapshots, keeping last {keep_last}.")
