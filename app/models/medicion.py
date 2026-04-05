from app.extensions import db


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
