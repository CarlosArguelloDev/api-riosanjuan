import json


def test_crear_medicion_valida(client, db):
    """POST /api/v1/mediciones con payload válido debe retornar 201."""
    payload = {
        "id_sensor": 999,
        "fecha_hora": "2025-10-14T09:30:00Z",
        "valor": 7.3,
    }
    resp = client.post(
        "/api/v1/mediciones",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["ok"] is True
    assert data["data"]["insertados"] == 1


def test_crear_medicion_batch(client, db):
    """POST /api/v1/mediciones con lista debe insertar todos los ítems."""
    payload = [
        {"id_sensor": 999, "fecha_hora": "2025-10-14T10:00:00Z", "valor": 8.0},
        {"id_sensor": 999, "fecha_hora": "2025-10-14T11:00:00Z", "valor": 9.1},
    ]
    resp = client.post(
        "/api/v1/mediciones",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201
    assert resp.get_json()["data"]["insertados"] == 2


def test_crear_medicion_payload_invalido(client):
    """POST /api/v1/mediciones sin JSON debe retornar 400."""
    resp = client.post("/api/v1/mediciones", data="not-json", content_type="text/plain")
    assert resp.status_code == 400
    assert resp.get_json()["ok"] is False


def test_consultar_mediciones_sin_id_sensor(client):
    """GET /api/v1/mediciones sin id_sensor debe retornar 400."""
    resp = client.get("/api/v1/mediciones")
    assert resp.status_code == 400
    assert resp.get_json()["ok"] is False


def test_consultar_mediciones(client, db):
    """GET /api/v1/mediciones con id_sensor debe retornar 200."""
    resp = client.get("/api/v1/mediciones?id_sensor=999")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert isinstance(data["data"], list)
