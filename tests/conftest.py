import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.routes import _service


@pytest.fixture(autouse=True)
def clean_store():
    """Reset storage (memory + disk) before every test."""
    _service._store.clear()
    yield
    _service._store.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_expense():
    return {
        "title": "Coffee",
        "amount": 4.50,
        "category": "food",
        "date": "2026-08-01",
    }
