from uuid import uuid4

from src.models import ExpenseCreate, Expense, ExpenseTotal
from src.storage import ExpenseStore
from src.errors import NotFoundError


class ExpenseService:
    """Pure business logic. No HTTP awareness. No storage implementation awareness."""

    def __init__(self, store: ExpenseStore):
        self._store = store

    def create_expense(self, data: ExpenseCreate) -> Expense:
        expense = Expense(
            id=str(uuid4()),
            title=data.title,
            amount=data.amount,
            category=data.category.lower().strip(),
            date=data.date,
        )
        self._store.add(expense.model_dump())
        return expense

    def get_all_expenses(self) -> list[Expense]:
        return [Expense(**e) for e in self._store.get_all()]

    def get_by_category(self, category: str) -> list[Expense]:
        category = category.lower().strip()
        return [Expense(**e) for e in self._store.get_all() if e["category"] == category]

    def get_totals(self) -> ExpenseTotal:
        all_expenses = self._store.get_all()
        overall = sum(e["amount"] for e in all_expenses)
        by_category: dict[str, float] = {}
        for e in all_expenses:
            cat = e["category"]
            by_category[cat] = by_category.get(cat, 0) + e["amount"]
        return ExpenseTotal(overall=round(overall, 2), by_category=by_category)

    def delete_expense(self, expense_id: str) -> None:
        if not self._store.delete(expense_id):
            raise NotFoundError(expense_id)
