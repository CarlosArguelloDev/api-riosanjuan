import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

# Base configuration
app = Flask(__name__)

db = SQLAlchemy(app)

@app.post("/measurements")
def create_measurements():
    """
    Receives ONE measurement or an ARRAY of measurements.
    Expected JSON body:
    {
      "id_sensor": 1,
      "timestamp": "2025-10-14T09:30:00Z",
      "value": 7.3
    }
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return fail("Invalid or empty JSON", 400)

    # Allow single or batch input
    items = payload if isinstance(payload, list) else [payload]

    measurements = []
    for i, item in enumerate(items, start=1):
        try:
            id_sensor = int(item["id_sensor"])
            timestamp = parse_iso_datetime(item["timestamp"])
            value = float(item["value"])
        except (KeyError, ValueError) as e:
            return fail(f"Item #{i} invalid: {e}", 400)

        measurements.append(Measurement(id_sensor=id_sensor, timestamp=timestamp, value=value))

    try:
        for m in measurements:
            db.session.merge(m)  # upsert by PK (id_sensor, timestamp)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # If it violates FK (nonexistent sensor) or format, it will fall here
        return fail("Could not save measurements", 400, str(e))

    return ok({"inserted": len(measurements)}, 201)

@app.get("/measurements")
def get_measurements():
    """
    Query parameters:
      - id_sensor (required)
      - from (start date)
      - to (end date)
      - limit (default 100)
      - order (asc|desc, default desc)
    """
    id_sensor = request.args.get("id_sensor", type=int)
    if not id_sensor:
        return fail("Parameter 'id_sensor' is required", 400)

    limit = request.args.get("limit", default=100, type=int)
    order = request.args.get("order", default="desc", type=str).lower()
    date_from = request.args.get("from")
    date_to = request.args.get("to")

    try:
        q = db.select(Measurement).where(Measurement.id_sensor == id_sensor)

        if date_from:
            q = q.where(Measurement.timestamp >= parse_iso_datetime(date_from))
        if date_to:
            q = q.where(Measurement.timestamp <= parse_iso_datetime(date_to))

        if order == "asc":
            q = q.order_by(Measurement.timestamp.asc())
        else:
            q = q.order_by(Measurement.timestamp.desc())

        q = q.limit(limit)

        rows = db.session.execute(q).scalars().all()
        data = [
            {
                "id_sensor": r.id_sensor,
                "timestamp": r.timestamp.isoformat(),
                "value": r.value,
            }
            for r in rows
        ]
        return ok(data)
    except ValueError as e:
        return fail(str(e), 400)
    except Exception as e:
        return fail("Error while querying measurements", 400, str(e))

if __name__ == "__main__":
    app.run(debug=True)
