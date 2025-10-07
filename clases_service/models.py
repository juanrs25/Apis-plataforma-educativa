from datetime import datetime
from db import db

class Clase(db.Model):
    __tablename__ = 'clases'

    id_clase = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    profesor_id = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Enum('Activa', 'Inactiva', 'Finalizada'), default='Activa')

    def to_dict(self):
        return {
            "id_clase": self.id_clase,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "profesor_id": self.profesor_id,
            "precio": float(self.precio or 0),
            "fecha_creacion": self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_creacion else None,
            "estado": self.estado
        }
