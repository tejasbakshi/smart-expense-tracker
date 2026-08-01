def test_filter_by_category(client, sample_expense):
    client.post("/expenses/", json=sample_expense)
    client.post("/expenses/", json={**sample_expense, "category": "transport", "title": "Bus"})
    response = client.get("/expenses/?category=food")
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "food"


def test_filter_case_insensitive(client, sample_expense):
    client.post("/expenses/", json=sample_expense)
    response = client.get("/expenses/?category=FOOD")
    assert len(response.json()) == 1


def test_filter_strips_whitespace(client, sample_expense):
    client.post("/expenses/", json=sample_expense)
    response = client.get("/expenses/?category= food ")
    assert len(response.json()) == 1


def test_filter_nonexistent_category_returns_empty(client, sample_expense):
    client.post("/expenses/", json=sample_expense)
    response = client.get("/expenses/?category=entertainment")
    assert response.status_code == 200
    assert response.json() == []
