from task import Task
from validator import validate_title, validate_id
from storage import load_tasks, save_tasks, DEFAULT_FILE


class TaskManager:
    """Mengelola tambah, selesai, hapus, dan daftar tugas."""

    def __init__(self, filepath=DEFAULT_FILE):
        self.filepath = filepath
        self.tasks = load_tasks(filepath)

    def _next_id(self):
        return max((t.id for t in self.tasks), default=0) + 1

    def _find(self, task_id):
        number = validate_id(task_id)
        for task in self.tasks:
            if task.id == number:
                return task
        raise ValueError(f"Tugas dengan ID {number} tidak ditemukan.")

    def add_task(self, title):
        task = Task(id=self._next_id(), title=validate_title(title))
        self.tasks.append(task)
        save_tasks(self.tasks, self.filepath)
        return task

    def complete_task(self, task_id):
        task = self._find(task_id)
        task.done = True
        save_tasks(self.tasks, self.filepath)
        return task

    def delete_task(self, task_id):
        task = self._find(task_id)
        self.tasks.remove(task)
        save_tasks(self.tasks, self.filepath)
        return task

    def list_tasks(self):
        return list(self.tasks)