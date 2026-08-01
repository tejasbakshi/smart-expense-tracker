def test_negative_amount_rejected(client, sample_expense):
    response = client.post("/expenses/", json={**sample_expense, "amount": -5})
    assert response.status_code == 422


def test_zero_amount_rejected(client, sample_expense):
    response = client.post("/expenses/", json={**sample_expense, "amount": 0})
    assert response.status_code == 422


def test_empty_title_rejected(client, sample_expense):
    response = client.post("/expenses/", json={**sample_expense, "title": ""})
    assert response.status_code == 422


def test_missing_title_rejected(client, sample_expense):
    payload = {"amount": 5.0, "category": "food", "date": "2026-08-01"}
    response = client.post("/expenses/", json=payload)
    assert response.status_code == 422


def test_missing_amount_rejected(client, sample_expense):
    payload = {"title": "Coffee", "category": "food", "date": "2026-08-01"}
    response = client.post("/expenses/", json=payload)
    assert response.status_code == 422


def test_missing_category_rejected(client, sample_expense):
    payload = {"title": "Coffee", "amount": 5.0, "date": "2026-08-01"}
    response = client.post("/expenses/", json=payload)
    assert response.status_code == 422


def test_missing_date_rejected(client, sample_expense):
    payload = {"title": "Coffee", "amount": 5.0, "category": "food"}
    response = client.post("/expenses/", json=payload)
    assert response.status_code == 422


def test_invalid_date_rejected(client, sample_expense):
    response = client.post("/expenses/", json={**sample_expense, "date": "not-a-date"})
    assert response.status_code == 422


def test_empty_body_rejected(client):
    response = client.post("/expenses/", json={})
    assert response.status_code == 422
