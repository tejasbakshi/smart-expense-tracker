import json
from pathlib import Path
from threading import Lock


class ExpenseStore:
    """Thread-safe JSON file store with dict keyed by expense ID."""

    def __init__(self, filepath: Path | None = None):
        self._filepath = filepath or (Path(__file__).resolve().parent.parent / "data" / "expenses.json")
        self._filepath.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._expenses: dict[str, dict] = {}
        self._load()

    def _load(self):
        if self._filepath.exists():
            with open(self._filepath) as f:
                content = f.read().strip()
                if not content:
                    return
                data = json.loads(content)
                self._expenses = {e["id"]: e for e in data}

    def _save(self):
        self._filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self._filepath, "w") as f:
            json.dump(list(self._expenses.values()), f, indent=2, default=str)

    def add(self, expense: dict) -> dict:
        with self._lock:
            self._expenses[expense["id"]] = expense
            self._save()
            return expense

    def get_all(self) -> list[dict]:
        with self._lock:
            return list(self._expenses.values())

    def get_by_id(self, expense_id: str) -> dict | None:
        with self._lock:
            return self._expenses.get(expense_id)

    def delete(self, expense_id: str) -> bool:
        with self._lock:
            if expense_id in self._expenses:
                del self._expenses[expense_id]
                self._save()
                return True
            return False

    def clear(self):
        with self._lock:
            self._expenses.clear()
            self._save()
