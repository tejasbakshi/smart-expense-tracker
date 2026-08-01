# Smart Expense Tracker API

A REST API for managing personal expenses, built with FastAPI and Python.

## Features

- Add, view, filter, and delete expenses
- Calculate total expenses (overall and by category)
- Input validation with clear error messages
- Category normalization (case-insensitive, whitespace-trimmed)
- JSON file persistence (data survives server restarts)
- Automatic OpenAPI/Swagger documentation
- Health check endpoint
- Thread-safe storage with concurrent request handling

## Prerequisites

- Python 3.11 or higher (tested on Python 3.13)
- If `python3 -m venv` fails, install it:

```bash
sudo dnf install python3-venv      # Fedora
sudo apt install python3-venv      # Ubuntu/Debian


Create and activate virtual environment

bash
python3 -m venv venv
source venv/bin/activate
python3 -m venv venv
source venv/bin/activate

Install dependencies

bash
pip install -r requirements.txt
pip install -r requirements.txt

Start the server

bash
python3 -m uvicorn src.main:app --host 127.0.0.1 --port 8000
python3 -m uvicorn src.main:app --host 127.0.0.1 --port 8000

Run tests

bash
python3 -m pytest tests/ -v
python3 -m pytest tests/ -v

API Documentation

Once the server is running, visit:


Swagger UI:
http://127.0.0.1:8000/docs
ReDoc:
http://127.0.0.1:8000/redoc

API Endpoints

Method	Path	Description	Status Code
GET	/health	Health check	200
POST	/expenses/	Add an expense	201
GET	/expenses/	View all expenses	200
GET	/expenses/?category=X	Filter by category	200
GET	/expenses/totals	Total expenses (overall and by category)	200
DELETE	/expenses/{id}	Delete an expense	204

Usage Examples

Create an expense

bash
curl -X POST http://127.0.0.1:8000/expenses/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Coffee", "amount": 4.50, "category": "food", "date": "2026-08-01"}'
curl -X POST http://127.0.0.1:8000/expenses/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Coffee", "amount": 4.50, "category": "food", "date": "2026-08-01"}'

Response (201 Created):


json
{
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "title": "Coffee",
    "amount": 4.50,
    "category": "food",
    "date": "2026-08-01"
}
{
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "title": "Coffee",
    "amount": 4.50,
    "category": "food",
    "date": "2026-08-01"
}

List all expenses

bash
curl http://127.0.0.1:8000/expenses/
curl http://127.0.0.1:8000/expenses/

Filter by category

bash
curl http://127.0.0.1:8000/expenses/?category=food
curl http://127.0.0.1:8000/expenses/?category=food

Get totals

bash
curl http://127.0.0.1:8000/expenses/totals
curl http://127.0.0.1:8000/expenses/totals

Response:


json
{
    "overall": 42.50,
    "by_category": {
        "food": 30.00,
        "transport": 12.50
    }
}
{
    "overall": 42.50,
    "by_category": {
        "food": 30.00,
        "transport": 12.50
    }
}

Delete an expense

bash
curl -X DELETE http://127.0.0.1:8000/expenses/a1b2c3d4-e5f6-7890-abcd-ef1234567890
curl -X DELETE http://127.0.0.1:8000/expenses/a1b2c3d4-e5f6-7890-abcd-ef1234567890

Error responses

All errors follow RFC 9457 vocabulary:


json
{
    "title": "NotFound",
    "detail": "Expense with id 'abc-123' not found",
    "status": 404
}
{
    "title": "NotFound",
    "detail": "Expense with id 'abc-123' not found",
    "status": 404
}

Project Structure

text
expense-tracker/
├── README.md
├── AI_NOTES.md
├── requirements.txt
├── data/
│   └── expenses.json          # Created at runtime
├── src/
│   ├── __init__.py
│   ├── main.py                # Application entry point
│   ├── models.py              # Pydantic schemas
│   ├── errors.py              # Exception hierarchy and error handler
│   ├── storage.py             # JSON file store (thread-safe)
│   ├── services.py            # Business logic
│   └── routes.py              # API endpoints
└── tests/
    ├── __init__.py
    ├── conftest.py            # Test fixtures
    ├── test_create.py         # POST /expenses
    ├── test_read.py           # GET /expenses
    ├── test_filter.py         # GET /expenses?category=
    ├── test_totals.py         # GET /expenses/totals
    ├── test_delete.py         # DELETE /expenses/{id}
    ├── test_validation.py     # Input validation (422)
    └── test_edge_cases.py     # Edge cases and health check
expense-tracker/
├── README.md
├── AI_NOTES.md
├── requirements.txt
├── data/
│   └── expenses.json          # Created at runtime
├── src/
│   ├── __init__.py
│   ├── main.py                # Application entry point
│   ├── models.py              # Pydantic schemas
│   ├── errors.py              # Exception hierarchy and error handler
│   ├── storage.py             # JSON file store (thread-safe)
│   ├── services.py            # Business logic
│   └── routes.py              # API endpoints
└── tests/
    ├── __init__.py
    ├── conftest.py            # Test fixtures
    ├── test_create.py         # POST /expenses
    ├── test_read.py           # GET /expenses
    ├── test_filter.py         # GET /expenses?category=
    ├── test_totals.py         # GET /expenses/totals
    ├── test_delete.py         # DELETE /expenses/{id}
    ├── test_validation.py     # Input validation (422)
    └── test_edge_cases.py     # Edge cases and health check

Tech Stack

Python 3.13 — Runtime
FastAPI — Web framework
Pydantic v2 — Data validation and serialization
Uvicorn — ASGI server
pytest — Testing framework
httpx — HTTP client for tests

Design Decisions

JSON file storage over in-memory — data survives server restarts
Thread-safe storage with threading.Lock — prevents race conditions under concurrent requests
Two Pydantic models (ExpenseCreate / Expense) — client never controls IDs
Custom exception hierarchy — separates business logic from HTTP concerns
RFC 9457 vocabulary in error responses — aligns with current API standards without full spec overhead
Category normalization — .lower().strip() on create and filter prevents inconsistent categories
