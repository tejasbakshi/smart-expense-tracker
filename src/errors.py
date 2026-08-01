from fastapi import Request
from fastapi.responses import JSONResponse


class ExpenseError(Exception):
    """Base exception for all expense tracker domain errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code


class NotFoundError(ExpenseError):
    """Raised when an expense ID does not exist in the store."""

    def __init__(self, expense_id: str):
        super().__init__(
            message=f"Expense with id '{expense_id}' not found",
            status_code=404,
        )


class ValidationError(ExpenseError):
    """Raised when business logic validation fails."""

    def __init__(self, message: str):
        super().__init__(message=message, status_code=422)


async def expense_error_handler(request: Request, exc: ExpenseError) -> JSONResponse:
    """Global handler that converts domain exceptions to RFC 9457 vocabulary responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "title": type(exc).__name__,
            "detail": exc.message,
            "status": exc.status_code,
        },
    )
