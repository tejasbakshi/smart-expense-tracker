# Smart Expense Tracker API

A REST API for managing personal expenses, built with FastAPI and Python.

## Features

- Add, view, filter, and delete expenses
- Calculate total expenses (overall and by category)
- Input validation with clear error messages
- Category normalization (case-insensitive, whitespace-trimmed)
- JSON file persistence (data survives server restarts)
- Automatic OpenAPI/Swagger documentation

## Prerequisites

- Python 3.11 or higher (tested on Python 3.13)
- If `python3 -m venv` fails, install it:
  ```bash
  sudo dnf install python3-venv      # Fedora
  sudo apt install python3-venv      # Ubuntu/Debian
