import json


def test_crear_prediccion_valida(client, db):
    """POST /api/v1/predicciones con payload válido debe retornar 201."""
    payload = {
        "id_sensor": 999,
        "fecha_objetivo": "2025-11-27T12:00:00Z",
        "valor_predicho": 23.5,
        "emitido_en": "2025-11-27T10:00:00Z",
    }
    resp = client.post(
        "/api/v1/predicciones",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["ok"] is True
    assert data["data"]["insertados"] == 1


def test_crear_prediccion_batch(client, db):
    """POST /api/v1/predicciones con lista debe insertar todos los ítems."""
    payload = [
        {
            "id_sensor": 999,
            "fecha_objetivo": "2025-11-28T12:00:00Z",
            "valor_predicho": 24.0,
            "emitido_en": "2025-11-27T10:00:00Z",
        },
        {
            "id_sensor": 999,
            "fecha_objetivo": "2025-11-29T12:00:00Z",
            "valor_predicho": 25.0,
            "emitido_en": "2025-11-27T10:00:00Z",
        },
    ]
    resp = client.post(
        "/api/v1/predicciones",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201
    assert resp.get_json()["data"]["insertados"] == 2


def test_consultar_predicciones_sin_id_sensor(client):
    """GET /api/v1/predicciones sin id_sensor debe retornar 400."""
    resp = client.get("/api/v1/predicciones")
    assert resp.status_code == 400
    assert resp.get_json()["ok"] is False


def test_consultar_predicciones(client, db):
    """GET /api/v1/predicciones con id_sensor debe retornar 200 y lista."""
    resp = client.get("/api/v1/predicciones?id_sensor=999")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert isinstance(data["data"], list)
