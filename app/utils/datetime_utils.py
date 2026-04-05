from datetime import datetime, timezone


def parse_iso_datetime(value: str) -> datetime:
    """
    Parsea ISO 8601. Acepta 'Z' como sufijo UTC.
    Si la fecha viene sin zona horaria, asume UTC.
    Lanza ValueError con mensaje amigable si el formato es inválido.
    """
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        raise ValueError(
            "La fecha debe estar en formato ISO 8601 (ej: 2025-10-14T09:30:00Z)"
        )
