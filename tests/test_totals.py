def test_totals_empty(client):
    response = client.get("/expenses/totals")
    assert response.status_code == 200
    data = response.json()
    assert data["overall"] == 0
    assert data["by_category"] == {}


def test_totals_single_expense(client, sample_expense):
    client.post("/expenses/", json=sample_expense)
    data = client.get("/expenses/totals").json()
    assert data["overall"] == 4.50
    assert data["by_category"] == {"food": 4.50}


def test_totals_multiple_categories(client, sample_expense):
    client.post("/expenses/", json=sample_expense)
    client.post("/expenses/", json={**sample_expense, "category": "transport", "amount": 10.00})
    data = client.get("/expenses/totals").json()
    assert data["overall"] == 14.50
    assert data["by_category"]["food"] == 4.50
    assert data["by_category"]["transport"] == 10.00


def test_totals_rounding(client, sample_expense):
    client.post("/expenses/", json={**sample_expense, "amount": 1.11})
    client.post("/expenses/", json={**sample_expense, "amount": 2.22})
    client.post("/expenses/", json={**sample_expense, "amount": 3.33})
    data = client.get("/expenses/totals").json()
    assert data["overall"] == 6.66


def test_totals_after_delete(client, sample_expense):
    r = client.post("/expenses/", json=sample_expense)
    eid = r.json()["id"]
    client.post("/expenses/", json={**sample_expense, "title": "Lunch", "amount": 12.00})
    client.delete(f"/expenses/{eid}")
    data = client.get("/expenses/totals").json()
    assert data["overall"] == 12.00
