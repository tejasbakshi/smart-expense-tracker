def test_list_empty_returns_empty_array(client):
    response = client.get("/expenses/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_returns_all_expenses(client, sample_expense):
    client.post("/expenses/", json=sample_expense)
    client.post("/expenses/", json={**sample_expense, "title": "Lunch"})
    response = client.get("/expenses/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_contains_correct_fields(client, sample_expense):
    client.post("/expenses/", json=sample_expense)
    data = response = client.get("/expenses/").json()[0]
    assert set(data.keys()) == {"id", "title", "amount", "category", "date"}
