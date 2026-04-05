from app.extensions import db


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
