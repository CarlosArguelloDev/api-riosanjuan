from flask import jsonify


def ok(data=None, status: int = 200):
    """Respuesta estándar de éxito."""
    return jsonify({"ok": True, "data": data}), status


def fail(message: str, status: int = 400, details=None):
    """Respuesta estándar de error."""
    payload = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status
