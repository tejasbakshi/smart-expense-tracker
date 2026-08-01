from pydantic import BaseModel, Field
from datetime import date


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    date: date


class Expense(BaseModel):
    id: str
    title: str
    amount: float
    category: str
    date: date


class ExpenseTotal(BaseModel):
    overall: float
    by_category: dict[str, float]
