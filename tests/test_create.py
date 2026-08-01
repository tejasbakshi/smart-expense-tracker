from src.routes import _service


def test_create_expense_returns_201(client, sample_expense):
    response = client.post("/expenses/", json=sample_expense)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Coffee"
    assert data["amount"] == 4.50
    assert data["category"] == "food"
    assert data["date"] == "2026-08-01"
    assert "id" in data


def test_create_expense_has_uuid_id(client, sample_expense):
    response = client.post("/expenses/", json=sample_expense)
    expense_id = response.json()["id"]
    assert len(expense_id) == 36
    assert expense_id.count("-") == 4


def test_create_expense_persists(client, sample_expense):
    client.post("/expenses/", json=sample_expense)
    response = client.get("/expenses/")
    assert len(response.json()) == 1
