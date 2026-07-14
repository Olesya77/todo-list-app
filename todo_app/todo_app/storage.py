import json
import os
from typing import List
from models import Task

DATA_FILE = "tasks.json"

def load_tasks() -> List[Task]:
    """
    Загружает список задач из файла tasks.json.
    Если файл не существует или повреждён, возвращает пустой список.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task.from_dict(item) for item in data.get("tasks", [])]
    except (json.JSONDecodeError, KeyError):
        return []

def save_tasks(tasks: List[Task]) -> None:
    """Сохраняет список задач в файл tasks.json в формате JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"tasks": [t.to_dict() for t in tasks]}, f, indent=2, ensure_ascii=False)

def get_next_id(tasks: List[Task]) -> int:
    """Возвращает следующий свободный идентификатор (максимальный id + 1)."""
    return max((t.id for t in tasks), default=0) + 1
