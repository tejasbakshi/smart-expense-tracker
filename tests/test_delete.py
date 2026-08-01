def test_delete_returns_204(client, sample_expense):
    r = client.post("/expenses/", json=sample_expense)
    eid = r.json()["id"]
    response = client.delete(f"/expenses/{eid}")
    assert response.status_code == 204


def test_delete_removes_from_store(client, sample_expense):
    r = client.post("/expenses/", json=sample_expense)
    eid = r.json()["id"]
    client.delete(f"/expenses/{eid}")
    assert len(client.get("/expenses/").json()) == 0


def test_delete_nonexistent_returns_404(client):
    response = client.delete("/expenses/nonexistent-id")
    assert response.status_code == 404
    data = response.json()
    assert data["title"] == "NotFoundError"
    assert "nonexistent-id" in data["detail"]


def test_delete_does_not_affect_other_expenses(client, sample_expense):
    r1 = client.post("/expenses/", json=sample_expense)
    r2 = client.post("/expenses/", json={**sample_expense, "title": "Lunch"})
    client.delete(f"/expenses/{r1.json()['id']}")
    remaining = client.get("/expenses/").json()
    assert len(remaining) == 1
    assert remaining[0]["title"] == "Lunch"
