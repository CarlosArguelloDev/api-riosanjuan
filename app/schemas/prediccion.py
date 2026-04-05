from app.utils.datetime_utils import parse_iso_datetime


def deserializar_prediccion(item: dict, index: int) -> dict:
    """
    Valida y deserializa un dict crudo de predicción.
    Lanza ValueError si falta algún campo o el formato es inválido.
    """
    try:
        return {
            "id_sensor": int(item["id_sensor"]),
            "fecha_objetivo": parse_iso_datetime(item["fecha_objetivo"]),
            "valor_predicho": float(item["valor_predicho"]),
            "emitido_en": parse_iso_datetime(item["emitido_en"]),
        }
    except (KeyError, ValueError) as e:
        raise ValueError(f"Ítem #{index} inválido: {e}")


def serializar_prediccion(r) -> dict:
    """Convierte un objeto Prediccion (ORM) o Row a JSON serializable."""
    return {
        "id_prediccion": r.id_prediccion,
        "id_sensor": r.id_sensor,
        "fecha_objetivo": r.fecha_objetivo.isoformat(),
        "valor_predicho": r.valor_predicho,
        "emitido_en": r.emitido_en.isoformat(),
    }
