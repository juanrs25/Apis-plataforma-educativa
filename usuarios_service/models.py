from db import db

class Rol(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    usuarios = db.relationship('Usuario', back_populates='rol')

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    Usuario = db.Column(db.String(255), nullable=False)
    Clave = db.Column(db.String(255), nullable=False)
    Nombre_Completo = db.Column(db.String(255), nullable=False)
    Telefono = db.Column(db.String(15), nullable=False)
    Direccion = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    experiencia_laboral = db.Column(db.Text)
    hoja_vida_path = db.Column(db.String(255))
    titulo_profesional = db.Column(db.String(100))
    estado_verificacion = db.Column(db.Enum('Pendiente', 'Verificado', 'Rechazado'), default='Pendiente')

    rol = db.relationship('Rol', back_populates='usuarios')
