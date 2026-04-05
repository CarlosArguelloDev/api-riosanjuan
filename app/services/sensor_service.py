from app.extensions import db
from app.models.tipo_sensor import TipoSensor
from app.models.sensor import Sensor


class TipoSensorService:
    @staticmethod
    def listar() -> list[dict]:
        rows = (
            db.session.execute(
                db.select(
                    TipoSensor.id_tipo_sensor,
                    TipoSensor.nombre,
                    TipoSensor.descripcion,
                    TipoSensor.unidad,
                    TipoSensor.valor_minimo,
                    TipoSensor.valor_maximo,
                    TipoSensor.decimales,
                ).order_by(TipoSensor.id_tipo_sensor)
            )
            .mappings()
            .all()
        )
        return list(map(dict, rows))


class SensorService:
    @staticmethod
    def listar(id_estacion: int | None = None, id_tipo_sensor: int | None = None) -> list[dict]:
        q = db.select(
            Sensor.id_sensor,
            Sensor.id_estacion,
            Sensor.id_tipo_sensor,
            Sensor.modelo,
            Sensor.numero_serie,
            Sensor.unidad_medida,
            Sensor.activo,
        ).order_by(Sensor.id_sensor)

        if id_estacion is not None:
            q = q.filter(Sensor.id_estacion == id_estacion)
        if id_tipo_sensor is not None:
            q = q.filter(Sensor.id_tipo_sensor == id_tipo_sensor)

        rows = db.session.execute(q).mappings().all()
        return list(map(dict, rows))
