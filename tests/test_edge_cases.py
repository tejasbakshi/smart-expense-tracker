def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_category_with_special_characters(client, sample_expense):
    client.post("/expenses/", json={**sample_expense, "category": "dining & drinks"})
    response = client.get("/expenses/", params={"category": "dining & drinks"})
    assert len(response.json()) == 1


def test_unicode_title(client, sample_expense):
    response = client.post("/expenses/", json={**sample_expense, "title": "Café au lait ☕"})
    assert response.status_code == 201
    assert response.json()["title"] == "Café au lait ☕"


def test_large_amount(client, sample_expense):
    response = client.post("/expenses/", json={**sample_expense, "amount": 999999.99})
    assert response.status_code == 201
    assert response.json()["amount"] == 999999.99


def test_category_normalization_stored_lowercase(client, sample_expense):
    client.post("/expenses/", json={**sample_expense, "category": "  FOOD  "})
    stored = client.get("/expenses/").json()[0]
    assert stored["category"] == "food"


def test_multiple_expenses_all_retrieved(client, sample_expense):
    for i in range(5):
        client.post("/expenses/", json={**sample_expense, "title": f"Item {i}", "amount": float(i + 1)})
    assert len(client.get("/expenses/").json()) == 5
