from app.extensions import db


class Prediccion(db.Model):
    __tablename__ = "predicciones"

    id_prediccion = db.Column(db.BigInteger, primary_key=True)
    id_sensor = db.Column(db.BigInteger, nullable=False)
    fecha_objetivo = db.Column(db.DateTime(timezone=True), nullable=False)
    valor_predicho = db.Column(db.Float, nullable=False)
    emitido_en = db.Column(db.DateTime(timezone=True), nullable=False)
