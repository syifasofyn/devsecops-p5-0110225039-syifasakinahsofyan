from dataclasses import dataclass, asdict


@dataclass
class Task:
    """Model data untuk satu tugas."""

    id: int
    title: str
    done: bool = False

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return Task(
            id=int(data["id"]),
            title=str(data["title"]),
            done=bool(data.get("done", False)),
        )