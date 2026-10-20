import json
import os

from task import Task

DEFAULT_FILE = "tasks.json"


def load_tasks(filepath=DEFAULT_FILE):
    """Membaca daftar tugas dari file JSON."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []
    return [Task.from_dict(item) for item in data]


def save_tasks(tasks, filepath=DEFAULT_FILE):
    """Menyimpan daftar tugas ke file JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2, ensure_ascii=False)