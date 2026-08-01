from fastapi import APIRouter, Query

from src.models import ExpenseCreate, Expense, ExpenseTotal
from src.services import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])

_service: ExpenseService | None = None


def init_routes(service: ExpenseService) -> None:
    global _service
    _service = service


@router.post("/", response_model=Expense, status_code=201)
def create_expense(data: ExpenseCreate):
    return _service.create_expense(data)


@router.get("/", response_model=list[Expense])
def list_expenses(category: str | None = Query(None)):
    if category:
        return _service.get_by_category(category)
    return _service.get_all_expenses()


@router.get("/totals", response_model=ExpenseTotal)
def get_totals():
    return _service.get_totals()


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: str):
    _service.delete_expense(expense_id)
