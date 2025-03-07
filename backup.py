import argparse
from database import init_db
from snapshot import snapshot
from restore import restore
from prune import prune

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup Tool")
    subparsers = parser.add_subparsers(dest="command")

    snap_parser = subparsers.add_parser("snapshot")
    snap_parser.add_argument("--target-directory", required=True)

    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument("--snapshot-id", type=int, required=True)
    restore_parser.add_argument("--restore-directory", required=True)

    prune_parser = subparsers.add_parser("prune")
    prune_parser.add_argument("--keep-last", type=int, required=True)

    args = parser.parse_args()
    init_db()

    if args.command == "snapshot":
        snapshot(args.target_directory)
    elif args.command == "restore":
        restore(args.snapshot_id, args.restore_directory)
    elif args.command == "prune":
        prune(args.keep_last)

# import os
# import sqlite3
# import hashlib
# import shutil
# from datetime import datetime
# from pathlib import Path
# import argparse

# # Initialize database
# DB_FILE = "backup.db"

# def init_db():
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS snapshots (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp TEXT NOT NULL
#         )
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS files (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             snapshot_id INTEGER,
#             path TEXT NOT NULL,
#             hash TEXT NOT NULL,
#             FOREIGN KEY(snapshot_id) REFERENCES snapshots(id)
#         )
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS file_data (
#             hash TEXT PRIMARY KEY,
#             content BLOB NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()

# def compute_hash(file_path):
#     hasher = hashlib.sha256()
#     with open(file_path, 'rb') as f:
#         while chunk := f.read(8192):
#             hasher.update(chunk)
#     return hasher.hexdigest()

# def snapshot(directory):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO snapshots (timestamp) VALUES (?)", (datetime.now().isoformat(),))
#     snapshot_id = cursor.lastrowid

#     for root, _, files in os.walk(directory):
#         for file in files:
#             file_path = os.path.join(root, file)
#             file_hash = compute_hash(file_path)

#             cursor.execute("SELECT hash FROM file_data WHERE hash = ?", (file_hash,))
#             if not cursor.fetchone():
#                 with open(file_path, 'rb') as f:
#                     cursor.execute("INSERT INTO file_data (hash, content) VALUES (?, ?)", (file_hash, f.read()))

#             cursor.execute("INSERT INTO files (snapshot_id, path, hash) VALUES (?, ?, ?)", (snapshot_id, file_path, file_hash))

#     conn.commit()
#     conn.close()
#     print(f"Snapshot {snapshot_id} created.")

# def restore(snapshot_id, restore_directory):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()

#     cursor.execute("SELECT path, hash FROM files WHERE snapshot_id = ?", (snapshot_id,))
#     files = cursor.fetchall()

#     if not files:
#         print("No snapshot found.")
#         return

#     os.makedirs(restore_directory, exist_ok=True)

#     for file_path, file_hash in files:
#         cursor.execute("SELECT content FROM file_data WHERE hash = ?", (file_hash,))
#         file_data = cursor.fetchone()
#         if file_data:
#             restore_path = os.path.join(restore_directory, os.path.relpath(file_path))
#             os.makedirs(os.path.dirname(restore_path), exist_ok=True)
#             with open(restore_path, 'wb') as f:
#                 f.write(file_data[0])

#     conn.close()
#     print(f"Snapshot {snapshot_id} restored to {restore_directory}.")

# def prune(keep_last):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()

#     cursor.execute("SELECT id FROM snapshots ORDER BY timestamp DESC LIMIT ? OFFSET ?", (keep_last, keep_last))
#     snapshots_to_delete = cursor.fetchall()

#     for (snapshot_id,) in snapshots_to_delete:
#         cursor.execute("DELETE FROM files WHERE snapshot_id = ?", (snapshot_id,))
#         cursor.execute("DELETE FROM snapshots WHERE id = ?", (snapshot_id,))

#     cursor.execute("DELETE FROM file_data WHERE hash NOT IN (SELECT DISTINCT hash FROM files)")

#     conn.commit()
#     conn.close()
#     print(f"Pruned old snapshots, keeping last {keep_last}.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Backup Tool")
#     subparsers = parser.add_subparsers(dest="command")

#     snap_parser = subparsers.add_parser("snapshot")
#     snap_parser.add_argument("--target-directory", required=True)

#     restore_parser = subparsers.add_parser("restore")
#     restore_parser.add_argument("--snapshot-id", type=int, required=True)
#     restore_parser.add_argument("--restore-directory", required=True)

#     prune_parser = subparsers.add_parser("prune")
#     prune_parser.add_argument("--keep-last", type=int, required=True)

#     args = parser.parse_args()
#     init_db()

#     if args.command == "snapshot":
#         snapshot(args.target_directory)
#     elif args.command == "restore":
#         restore(args.snapshot_id, args.restore_directory)
#     elif args.command == "prune":
#         prune(args.keep_last)
