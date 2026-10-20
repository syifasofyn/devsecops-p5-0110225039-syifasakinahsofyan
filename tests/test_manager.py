import os
import tempfile
import unittest

from manager import TaskManager
from validator import validate_title, validate_id


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.path)
        self.manager = TaskManager(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_add_task(self):
        task = self.manager.add_task("Belajar DevSecOps")
        self.assertEqual(task.id, 1)
        self.assertEqual(len(self.manager.list_tasks()), 1)

    def test_complete_task(self):
        self.manager.add_task("Kerjakan tugas")
        task = self.manager.complete_task(1)
        self.assertTrue(task.done)

    def test_delete_task(self):
        self.manager.add_task("Hapus saya")
        self.manager.delete_task(1)
        self.assertEqual(len(self.manager.list_tasks()), 0)

    def test_data_persisted(self):
        self.manager.add_task("Simpan ke file")
        reloaded = TaskManager(self.path)
        self.assertEqual(len(reloaded.list_tasks()), 1)

    def test_task_not_found(self):
        with self.assertRaises(ValueError):
            self.manager.complete_task(99)


class TestValidator(unittest.TestCase):
    def test_empty_title(self):
        with self.assertRaises(ValueError):
            validate_title("   ")

    def test_title_trimmed(self):
        self.assertEqual(validate_title("  halo  "), "halo")

    def test_invalid_id(self):
        with self.assertRaises(ValueError):
            validate_id("abc")
        with self.assertRaises(ValueError):
            validate_id(0)


if __name__ == "__main__":
    unittest.main()