from dataclasses import dataclass

@dataclass
class Task:
    """Модель задачи."""
    id: int
    title: str
    done: bool

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "done": self.done}

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(id=data["id"], title=data["title"], done=data["done"])
