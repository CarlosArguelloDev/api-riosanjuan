from flask import Blueprint, request
from app.services.sensor_service import TipoSensorService, SensorService
from app.utils.responses import ok

bp = Blueprint("sensores", __name__, url_prefix="/api/v1")


@bp.get("/tipos_sensor")
def listar_tipos_sensor():
    return ok(TipoSensorService.listar())


@bp.get("/sensores")
def listar_sensores():
    id_estacion = request.args.get("id_estacion", type=int)
    id_tipo_sensor = request.args.get("id_tipo_sensor", type=int)
    return ok(SensorService.listar(id_estacion, id_tipo_sensor))
