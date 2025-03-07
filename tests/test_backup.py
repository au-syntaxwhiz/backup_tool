import unittest
import os
import sqlite3
from backup import init_db, snapshot, restore, prune, DB_FILE
from pathlib import Path

TEST_DIR = "test_data"
RESTORE_DIR = "test_restore"

class TestBackupTool(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup test environment before tests run."""
        os.makedirs(TEST_DIR, exist_ok=True)
        with open(os.path.join(TEST_DIR, "test1.txt"), "w") as f:
            f.write("Hello, World!")

        with open(os.path.join(TEST_DIR, "test2.txt"), "w") as f:
            f.write("Backup test file.")

        init_db()

    @classmethod
    def tearDownClass(cls):
        """Cleanup test environment after all tests."""
        shutil.rmtree(TEST_DIR, ignore_errors=True)
        shutil.rmtree(RESTORE_DIR, ignore_errors=True)
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

    def test_snapshot(self):
        """Test that a snapshot is created and files are recorded in the database."""
        snapshot(TEST_DIR)

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM snapshots")
        snapshot_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM files")
        file_count = cursor.fetchone()[0]

        conn.close()

        self.assertGreater(snapshot_count, 0, "No snapshots were created.")
        self.assertGreater(file_count, 0, "No files were recorded in the snapshot.")

    def test_restore(self):
        """Test restoring a snapshot."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM snapshots ORDER BY id DESC LIMIT 1")
        snapshot_id = cursor.fetchone()[0]
        conn.close()

        restore(snapshot_id, RESTORE_DIR)

        self.assertTrue(os.path.exists(os.path.join(RESTORE_DIR, "test1.txt")), "File test1.txt was not restored.")
        self.assertTrue(os.path.exists(os.path.join(RESTORE_DIR, "test2.txt")), "File test2.txt was not restored.")

    def test_prune(self):
        """Test pruning snapshots."""
        prune(1)

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM snapshots")
        snapshot_count = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(snapshot_count, 1, "More than the expected number of snapshots were kept.")

if __name__ == "__main__":
    unittest.main()
