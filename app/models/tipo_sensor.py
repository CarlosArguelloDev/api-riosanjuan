from app.extensions import db


class TipoSensor(db.Model):
    __tablename__ = "tipos_sensor"

    id_tipo_sensor = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.Text, nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    unidad = db.Column(db.Text)
    valor_minimo = db.Column(db.Float)
    valor_maximo = db.Column(db.Float)
    decimales = db.Column(db.Integer)
