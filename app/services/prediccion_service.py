from sqlalchemy import func

from app.extensions import db
from app.models.prediccion import Prediccion
from app.schemas.prediccion import deserializar_prediccion, serializar_prediccion
from app.utils.datetime_utils import parse_iso_datetime


class PrediccionService:

    @staticmethod
    def crear(payload) -> int:
        """
        Acepta un dict o lista de dicts.
        Inserta sin upsert (preserva historial de predicciones).
        Retorna el número de registros insertados.
        """
        items = payload if isinstance(payload, list) else [payload]

        registros = []
        for i, item in enumerate(items, start=1):
            data = deserializar_prediccion(item, i)
            registros.append(Prediccion(**data))

        db.session.add_all(registros)
        db.session.commit()
        return len(registros)

    @staticmethod
    def consultar(
        id_sensor: int,
        desde_objetivo: str | None = None,
        hasta_objetivo: str | None = None,
        emitido_desde: str | None = None,
        emitido_hasta: str | None = None,
        latest: bool = False,
        limit: int = 100,
        order: str = "desc",
    ) -> list[dict]:
        """
        Consulta predicciones con múltiples filtros opcionales.
        Si latest=True, retorna solo la predicción más reciente por fecha_objetivo.
        """
        if latest:
            return PrediccionService._consultar_latest(
                id_sensor, desde_objetivo, hasta_objetivo,
                emitido_desde, emitido_hasta, limit, order
            )

        base = db.select(Prediccion).where(Prediccion.id_sensor == id_sensor)
        base = _aplicar_filtros_fechas(base, desde_objetivo, hasta_objetivo, emitido_desde, emitido_hasta)

        if order == "asc":
            base = base.order_by(Prediccion.fecha_objetivo.asc(), Prediccion.emitido_en.asc())
        else:
            base = base.order_by(Prediccion.fecha_objetivo.desc(), Prediccion.emitido_en.desc())

        base = base.limit(limit)
        rows = db.session.execute(base).scalars().all()
        return [serializar_prediccion(r) for r in rows]

    @staticmethod
    def _consultar_latest(
        id_sensor: int,
        desde_objetivo: str | None,
        hasta_objetivo: str | None,
        emitido_desde: str | None,
        emitido_hasta: str | None,
        limit: int,
        order: str,
    ) -> list[dict]:
        """ROW_NUMBER() para retener solo la predicción más reciente por fecha_objetivo."""
        rn = func.row_number().over(
            partition_by=Prediccion.fecha_objetivo,
            order_by=Prediccion.emitido_en.desc(),
        ).label("rn")

        sub = db.select(
            Prediccion.id_prediccion,
            Prediccion.id_sensor,
            Prediccion.fecha_objetivo,
            Prediccion.valor_predicho,
            Prediccion.emitido_en,
            rn,
        ).where(Prediccion.id_sensor == id_sensor)

        sub = _aplicar_filtros_fechas(sub, desde_objetivo, hasta_objetivo, emitido_desde, emitido_hasta)
        sub = sub.subquery()

        q = db.select(sub).where(sub.c.rn == 1)

        if order == "asc":
            q = q.order_by(sub.c.fecha_objetivo.asc(), sub.c.emitido_en.asc())
        else:
            q = q.order_by(sub.c.fecha_objetivo.desc(), sub.c.emitido_en.desc())

        q = q.limit(limit)
        rows = db.session.execute(q).all()
        return [serializar_prediccion(r) for r in rows]


def _aplicar_filtros_fechas(q, desde_objetivo, hasta_objetivo, emitido_desde, emitido_hasta):
    """Aplica filtros de rango de fechas a una query de Prediccion."""
    if desde_objetivo:
        q = q.where(Prediccion.fecha_objetivo >= parse_iso_datetime(desde_objetivo))
    if hasta_objetivo:
        q = q.where(Prediccion.fecha_objetivo <= parse_iso_datetime(hasta_objetivo))
    if emitido_desde:
        q = q.where(Prediccion.emitido_en >= parse_iso_datetime(emitido_desde))
    if emitido_hasta:
        q = q.where(Prediccion.emitido_en <= parse_iso_datetime(emitido_hasta))
    return q
