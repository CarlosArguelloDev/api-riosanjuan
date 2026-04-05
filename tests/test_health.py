def test_health_ok(client):
    """El endpoint /health debe responder 200 con status healthy."""
    resp = client.get("/health")
    # En testing con SQLite no hay problema de conexión
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
