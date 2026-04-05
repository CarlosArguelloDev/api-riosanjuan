from app.extensions import db


class Estacion(db.Model):
    __tablename__ = "estaciones"

    id_estacion = db.Column(db.BigInteger, primary_key=True)
    codigo = db.Column(db.Text, nullable=False, unique=True)
    nombre = db.Column(db.Text)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    activa = db.Column(db.Boolean, nullable=False, default=True)
