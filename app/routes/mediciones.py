from flask import Blueprint, request
from app.extensions import db
from app.services.medicion_service import MedicionService
from app.utils.responses import ok, fail

bp = Blueprint("mediciones", __name__, url_prefix="/api/v1")


@bp.post("/mediciones")
def crear_mediciones():
    payload = request.get_json(silent=True)
    if payload is None:
        return fail("JSON inválido o vacío", 400)

    try:
        insertados = MedicionService.crear(payload)
        return ok({"insertados": insertados}, 201)
    except ValueError as e:
        db.session.rollback()
        return fail(str(e), 400)
    except Exception as e:
        db.session.rollback()
        return fail("No se pudieron guardar las mediciones", 400, str(e))


@bp.get("/mediciones")
def consultar_mediciones():
    id_sensor = request.args.get("id_sensor", type=int)
    if not id_sensor:
        return fail("Parámetro 'id_sensor' es obligatorio", 400)

    try:
        data = MedicionService.consultar(
            id_sensor=id_sensor,
            desde=request.args.get("desde"),
            hasta=request.args.get("hasta"),
            limit=request.args.get("limit", default=100, type=int),
            order=request.args.get("order", default="desc").lower(),
        )
        return ok(data)
    except ValueError as e:
        return fail(str(e), 400)
    except Exception as e:
        return fail("Error al consultar mediciones", 500, str(e))
