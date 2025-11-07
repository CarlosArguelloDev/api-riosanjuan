import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
load_dotenv()

# Configuración base
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL","")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelos 
class Estacion(db.Model):
    __tablename__ = "estaciones"
    id_estacion = db.Column(db.BigInteger, primary_key=True)
    codigo = db.Column(db.Text, nullable=False, unique=True)
    nombre = db.Column(db.Text)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    activa = db.Column(db.Boolean, nullable=False, default=True)

class TipoSensor(db.Model):
    __tablename__ = "tipos_sensor"
    id_tipo_sensor = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.Text, nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    unidad = db.Column(db.Text)
    valor_minimo = db.Column(db.Float)
    valor_maximo = db.Column(db.Float)
    decimales = db.Column(db.Integer)

class Sensor(db.Model):
    __tablename__ = "sensores"
    id_sensor = db.Column(db.BigInteger, primary_key=True)
    id_estacion = db.Column(
        db.BigInteger, db.ForeignKey("estaciones.id_estacion", ondelete="SET NULL")
    )
    id_tipo_sensor = db.Column(
        db.BigInteger, db.ForeignKey("tipos_sensor.id_tipo_sensor", ondelete="SET NULL")
    )
    modelo = db.Column(db.Text)
    numero_serie = db.Column(db.Text)
    unidad_medida = db.Column(db.Text)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    estacion = db.relationship("Estacion", lazy="joined")
    tipo = db.relationship("TipoSensor", lazy="joined")

class Medicion(db.Model):
    __tablename__ = "mediciones"
    id_sensor = db.Column(
        db.BigInteger,
        db.ForeignKey("sensores.id_sensor", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    fecha_hora = db.Column(db.DateTime(timezone=True), primary_key=True, nullable=False)
    valor = db.Column(db.Float, nullable=False)


# ----------------------------------
# Helpers
# ----------------------------------
def parse_iso_datetime(value: str) -> datetime:
    """
    Acepta ISO 8601 (ej: '2025-10-14T09:30:00Z' o '2025-10-14 09:30:00+00:00').
    Si viene sin zona, se asume UTC.
    """
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            # Asumimos UTC si no trae tz
            from datetime import timezone

            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        raise ValueError("fecha_hora debe venir en formato ISO 8601 (ej: 2025-10-14T09:30:00Z)")

def ok(data=None, status=200):
    return jsonify({"ok": True, "data": data}), status

def fail(message, status=400, details=None):
    payload = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status


# ----------------------------------
# Rutas
# ----------------------------------
@app.get("/health")
def health():
    # ping sencillo a la DB
    db.session.execute(db.select(func.now()))
    return ok({"status": "healthy"})

# ------- Catálogos -------
@app.get("/estaciones")
def listar_estaciones():
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
    return ok(list(map(dict, rows)))

@app.get("/tipos_sensor")
def listar_tipos_sensor():
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
    return ok(list(map(dict, rows)))

@app.get("/sensores")
def listar_sensores():
    q = db.select(
        Sensor.id_sensor,
        Sensor.id_estacion,
        Sensor.id_tipo_sensor,
        Sensor.modelo,
        Sensor.numero_serie,
        Sensor.unidad_medida,
        Sensor.activo,
    ).order_by(Sensor.id_sensor)

    # Filtros opcionales
    id_estacion = request.args.get("id_estacion", type=int)
    id_tipo_sensor = request.args.get("id_tipo_sensor", type=int)
    if id_estacion is not None:
        q = q.filter(Sensor.id_estacion == id_estacion)
    if id_tipo_sensor is not None:
        q = q.filter(Sensor.id_tipo_sensor == id_tipo_sensor)

    rows = db.session.execute(q).mappings().all()
    return ok(list(map(dict, rows)))

# ------- Mediciones -------
@app.post("/mediciones")
def crear_mediciones():
    """
    Recibe UNA medición o un ARREGLO de mediciones.
    Cuerpo esperado (JSON):
    {
      "id_sensor": 1,
      "fecha_hora": "2025-10-14T09:30:00Z",
      "valor": 7.3
    }
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return fail("JSON inválido o vacío", 400)

    # Permitir single o batch
    items = payload if isinstance(payload, list) else [payload]

    mediciones = []
    for i, item in enumerate(items, start=1):
        try:
            id_sensor = int(item["id_sensor"])
            fecha_hora = parse_iso_datetime(item["fecha_hora"])
            valor = float(item["valor"])
        except (KeyError, ValueError) as e:
            return fail(f"Ítem #{i} inválido: {e}", 400)

        mediciones.append(Medicion(id_sensor=id_sensor, fecha_hora=fecha_hora, valor=valor))

    try:
        for m in mediciones:
            db.session.merge(m)  # upsert por PK (id_sensor, fecha_hora)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Si viola FK (sensor inexistente) o formato, caerá aquí
        return fail("No se pudieron guardar las mediciones", 400, str(e))

    return ok({"insertados": len(mediciones)}, 201)

@app.get("/mediciones")
def consultar_mediciones():
    """
    Parámetros:
      - id_sensor (obligatorio)
      - desde (ISO 8601 opcional)
      - hasta (ISO 8601 opcional)
      - limit (int, por defecto 100)
      - order (asc|desc, por defecto desc)
    """
    id_sensor = request.args.get("id_sensor", type=int)
    if not id_sensor:
        return fail("Parámetro 'id_sensor' es obligatorio", 400)

    limit = request.args.get("limit", default=100, type=int)
    order = request.args.get("order", default="desc", type=str).lower()
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    try:
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
        data = [
            {
                "id_sensor": r.id_sensor,
                "fecha_hora": r.fecha_hora.isoformat(),
                "valor": r.valor,
            }
            for r in rows
        ]
        return ok(data)
    except ValueError as e:
        return fail(str(e), 400)
    except Exception as e:
        return fail("Error al consultar mediciones", 400, str(e))


# ----------------------------------
# Punto de entrada
# ----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
