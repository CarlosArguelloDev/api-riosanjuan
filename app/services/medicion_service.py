from app.extensions import db
from app.models.medicion import Medicion
from app.schemas.medicion import deserializar_medicion, serializar_medicion
from app.utils.datetime_utils import parse_iso_datetime


class MedicionService:

    @staticmethod
    def crear(payload) -> int:
        """
        Acepta un dict o una lista de dicts.
        Hace upsert por PK (id_sensor, fecha_hora).
        Retorna el número de registros insertados/actualizados.
        """
        items = payload if isinstance(payload, list) else [payload]

        mediciones = []
        for i, item in enumerate(items, start=1):
            data = deserializar_medicion(item, i)
            mediciones.append(Medicion(**data))

        for m in mediciones:
            db.session.merge(m)
        db.session.commit()
        return len(mediciones)

    @staticmethod
    def consultar(
        id_sensor: int,
        desde: str | None = None,
        hasta: str | None = None,
        limit: int = 100,
        order: str = "desc",
    ) -> list[dict]:
        """Consulta mediciones con filtros opcionales de rango de fechas."""
        q = db.select(Medicion).where(Medicion.id_sensor == id_sensor)

        if desde:
            q = q.where(Medicion.fecha_hora >= parse_iso_datetime(desde))
        if hasta:
            q = q.where(Medicion.fecha_hora <= parse_iso_datetime(hasta))

        if order == "asc":
            q = q.order_by(Medicion.fecha_hora.asc())
        else:
            q = q.order_by(Medicion.fecha_hora.desc())

        q = q.limit(limit)
        rows = db.session.execute(q).scalars().all()
        return [serializar_medicion(r) for r in rows]
