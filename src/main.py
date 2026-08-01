import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.storage import ExpenseStore
from src.services import ExpenseService
from src.routes import router, init_routes
from src.errors import ExpenseError, expense_error_handler

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("expense_tracker")

store = ExpenseStore()
service = ExpenseService(store)
init_routes(service)

app = FastAPI(
    title="Smart Expense Tracker",
    description="REST API to manage personal expenses",
    version="1.0.0",
)

app.include_router(router)
app.exception_handler(ExpenseError)(expense_error_handler)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
