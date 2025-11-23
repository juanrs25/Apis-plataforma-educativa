from db import db
from datetime import datetime

class Inscripcion(db.Model):
    __tablename__ = "inscripciones"

    id_inscripcion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_clase = db.Column(db.Integer, nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Enum("Pendiente", "Aprobada", "Rechazada"), default="Pendiente")

    def to_dict(self):
        return {
            "id_inscripcion": self.id_inscripcion,
            "id_usuario": self.id_usuario,
            "id_clase": self.id_clase,
            "fecha_inscripcion": self.fecha_inscripcion.strftime("%Y-%m-%d %H:%M:%S"),
            "estado": self.estado
        }
