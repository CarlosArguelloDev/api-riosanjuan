from app.extensions import db
from app.models.estacion import Estacion


class EstacionService:
    @staticmethod
    def listar() -> list[dict]:
        rows = (
            db.session.execute(
                db.select(
                    Estacion.id_estacion,
                    Estacion.codigo,
                    Estacion.nombre,
                    Estacion.latitud,
                    Estacion.longitud,
                    Estacion.activa,
                ).order_by(Estacion.id_estacion)
            )
            .mappings()
            .all()
        )
        return list(map(dict, rows))
