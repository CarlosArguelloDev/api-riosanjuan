from flask import Blueprint
from app.services.estacion_service import EstacionService
from app.utils.responses import ok

bp = Blueprint("estaciones", __name__, url_prefix="/api/v1")


@bp.get("/estaciones")
def listar_estaciones():
    return ok(EstacionService.listar())
