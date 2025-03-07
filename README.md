# Backup Tool

## Overview
This is a command-line backup tool that provides functionality for creating file backups, restoring snapshots, and pruning old backups. It is designed to be efficient, using a SQLite database to track file snapshots and avoid redundant storage of duplicate files.

## Why I Chose This Tech Stack
- **Python**: Python was chosen due to its simplicity, built-in libraries for file handling, and strong community support.
- **SQLite**: A lightweight, file-based database to efficiently store metadata of snapshots without requiring an external database server.
- **argparse**: A built-in module for command-line argument parsing, making the tool user-friendly.
- **hashlib**: Used for generating SHA-256 hashes of files to track changes and avoid duplicate storage.
- **shutil & pathlib**: Used for file system operations such as copying and restoring files.

---

## Project Structure
```
.
├── backup.py        # Main entry point
├── database.py      # Handles database initialization and connections
├── prune.py         # Handles pruning old snapshots
├── restore.py       # Restores files from a snapshot
├── snapshot.py      # Creates file snapshots
├── utils.py         # Utility functions such as hash computation
├── tests            # Directory containing unit tests
│   ├── test_backup.py
│   
└── README.md        # Documentation
```

---

## Logic Behind Each File

### 1. `backup.py`
This is the main entry point for the backup tool. It provides a command-line interface to interact with the tool.
- Initializes the SQLite database.
- Provides commands for:
  - **`snapshot --target-directory`**: Creates a snapshot of the specified directory.
  - **`restore --snapshot-id --restore-directory`**: Restores files from a specific snapshot.
  - **`prune --keep-last`**: Deletes older snapshots while keeping the most recent ones.

### 2. `database.py`
- Initializes the SQLite database.
- Creates three tables:
  - `snapshots`: Stores snapshots with timestamps.
  - `files`: Stores file paths and their corresponding hashes.
  - `file_data`: Stores unique file contents to avoid redundant storage.

### 3. `prune.py`
- Deletes old snapshots while keeping the most recent ones.
- Ensures that orphaned files (files not associated with any snapshot) are deleted from the database.

### 4. `restore.py`
- Restores files from a specific snapshot.
- Ensures directory structure is recreated during restoration.
- Fetches file content from the database and writes it back to the filesystem.

### 5. `snapshot.py`
- Creates a new snapshot of a target directory.
- Computes SHA-256 hashes of files to track changes efficiently.
- Only stores file content if it hasn't been saved before (avoiding redundant storage).
- Stores file metadata (paths and hashes) in the database.

### 6. `utils.py`
- Contains helper functions such as:
  - `compute_hash(file_path)`: Computes the SHA-256 hash of a file to identify duplicates.
  - `get_latest_snapshot()`: Retrieves the latest snapshot ID.
  - `list_snapshots()`: Lists all available snapshots with timestamps.

---

## Test Cases
Tests are written using the `unittest` module.

### Tests Cover:
1. **Snapshot Creation**: Ensures files are correctly added to the database.
2. **Restoration**: Ensures files are restored correctly from snapshots.
3. **Pruning**: Ensures old snapshots are deleted correctly while preserving the required number.
4. **Database Integrity**: Ensures metadata consistency after operations.

To run tests:
```sh
python -m unittest discover tests
```

---

## What I Wanted to Achieve
- A simple, efficient command-line backup system.
- Avoid redundant storage by saving only unique file content.
- Ability to restore files from a specific point in time.
- Prune older snapshots to manage storage efficiently.

## Steps to Run the Project

1. **Install Python Dependencies** (if any are required):
   ```sh
   pip install -r requirements.txt  # If needed
   ```

2. **Initialize the Database**:
   ```sh
   python backup.py
   ```

3. **Take a Snapshot**:
   ```sh
   python backup.py snapshot --target-directory /path/to/directory
   ```

4. **List Snapshots**:
   ```sh
   python database.py list
   ```

5. **Restore Files from a Snapshot**:
   ```sh
   python backup.py restore --snapshot-id 1 --restore-directory /path/to/restore
   ```

6. **Prune Old Snapshots**:
   ```sh
   python backup.py prune --keep-last 3
   ```

---

This tool ensures efficient file backups while keeping storage optimized. 🚀

