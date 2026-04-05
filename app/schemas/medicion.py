from app.utils.datetime_utils import parse_iso_datetime


def deserializar_medicion(item: dict, index: int) -> dict:
    """
    Valida y deserializa un dict crudo de medición.
    Lanza ValueError si falta algún campo o el formato es inválido.
    """
    try:
        return {
            "id_sensor": int(item["id_sensor"]),
            "fecha_hora": parse_iso_datetime(item["fecha_hora"]),
            "valor": float(item["valor"]),
        }
    except (KeyError, ValueError) as e:
        raise ValueError(f"Ítem #{index} inválido: {e}")


def serializar_medicion(m) -> dict:
    """Convierte un objeto Medicion (ORM) o dict a JSON serializable."""
    if isinstance(m, dict):
        return {
            "id_sensor": m["id_sensor"],
            "fecha_hora": m["fecha_hora"].isoformat(),
            "valor": m["valor"],
        }
    return {
        "id_sensor": m.id_sensor,
        "fecha_hora": m.fecha_hora.isoformat(),
        "valor": m.valor,
    }
