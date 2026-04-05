from flask import Blueprint, request
from app.extensions import db
from app.services.prediccion_service import PrediccionService
from app.utils.responses import ok, fail

bp = Blueprint("predicciones", __name__, url_prefix="/api/v1")


@bp.post("/predicciones")
def crear_predicciones():
    payload = request.get_json(silent=True)
    if payload is None:
        return fail("JSON inválido o vacío", 400)

    try:
        insertados = PrediccionService.crear(payload)
        return ok({"insertados": insertados}, 201)
    except ValueError as e:
        db.session.rollback()
        return fail(str(e), 400)
    except Exception as e:
        db.session.rollback()
        return fail("No se pudieron guardar las predicciones", 400, str(e))


@bp.get("/predicciones")
def consultar_predicciones():
    id_sensor = request.args.get("id_sensor", type=int)
    if not id_sensor:
        return fail("Parámetro 'id_sensor' es obligatorio", 400)

    try:
        data = PrediccionService.consultar(
            id_sensor=id_sensor,
            desde_objetivo=request.args.get("desde_objetivo"),
            hasta_objetivo=request.args.get("hasta_objetivo"),
            emitido_desde=request.args.get("emitido_desde"),
            emitido_hasta=request.args.get("emitido_hasta"),
            latest=request.args.get("latest", default="false").lower() == "true",
            limit=request.args.get("limit", default=100, type=int),
            order=request.args.get("order", default="desc").lower(),
        )
        return ok(data)
    except ValueError as e:
        return fail(str(e), 400)
    except Exception as e:
        return fail("Error al consultar predicciones", 500, str(e))
