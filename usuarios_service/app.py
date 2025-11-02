from flask import Flask, jsonify, request
from flask_cors import CORS
from db import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from models import Usuario, Rol
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from config import SECRET_KEY

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

# ======================================
#  FUNCIONES DE AUTENTICACIÓN JWT
# ======================================

def token_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split(" ")

            # Si el header tiene formato "Bearer token"
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
            else:
                # Si solo viene el token sin 'Bearer'
                token = parts[0]

        if not token:
            return jsonify({'mensaje': 'Token es requerido'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            usuario_actual = Usuario.query.filter_by(id=data['id']).first()
        except Exception as e:
            return jsonify({'mensaje': 'Token es inválido', 'error': str(e)}), 401

        return f(usuario_actual, *args, **kwargs)
    return decorated




# ======================================
# RUTA DE PRUEBA
# ======================================
@app.route('/')
def index():
    return jsonify({"message": "API Usuarios corriendo con MySQL"})


# ======================================
# LOGIN (Generar token JWT)
# ======================================
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(Usuario=data['Usuario']).first()

    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    if not bcrypt.checkpw(data['Clave'].encode('utf-8'), usuario.Clave.encode('utf-8')):
        return jsonify({'message': 'Contraseña incorrecta'}), 401

    token = jwt.encode({
        'id': usuario.id,
        'rol': usuario.rol.nombre,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'message': 'Inicio de sesión exitoso',
        'token': token,
        'rol': usuario.rol.nombre
    }), 200



# PERFIL DEL USUARIO (Cliente autenticado)

@app.route('/perfil', methods=['GET'])
@token_requerido
def perfil(usuario):
    return jsonify({
        'id': usuario.id,
        'Usuario': usuario.Usuario,
        'Nombre_Completo': usuario.Nombre_Completo,
        'Email': usuario.Email,
        'rol': usuario.rol.nombre
    }), 200



# RUTAS SOLO PARA ADMINISTRADOR

@app.route('/usuarios', methods=['GET'])
@token_requerido
def get_usuarios(usuario):
    if usuario.rol.nombre != 'Admin':
        return jsonify({'message': 'No tienes permisos para acceder a esta ruta'}), 403

    usuarios = Usuario.query.all()
    return jsonify([{
        'id': u.id,
        'Usuario': u.Usuario,
        'Nombre_Completo': u.Nombre_Completo,
        'Email': u.Email,
        'rol': u.rol.nombre if u.rol else None,
        'estado_verificacion': u.estado_verificacion
    } for u in usuarios])


@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
@token_requerido
def get_usuario(usuario, id_usuario):
    if usuario.rol.nombre != 'Administrador':
        return jsonify({'message': 'Acceso denegado'}), 403

    user = Usuario.query.get(id_usuario)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        'id': user.id,
        'Usuario': user.Usuario,
        'Nombre_Completo': user.Nombre_Completo,
        'Email': user.Email,
        'rol': user.rol.nombre if user.rol else None,
        'estado_verificacion': user.estado_verificacion
    }), 200


@app.route('/usuarios', methods=['POST'])
@token_requerido
def create_usuario(usuario):
    if usuario.rol.nombre != 'Administrador':
        return jsonify({'message': 'Solo los administradores pueden crear usuarios'}), 403

    try:
        data = request.get_json()
        password = data['Clave'].encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        nuevo = Usuario(
            Usuario=data['Usuario'],
            Clave=hashed.decode('utf-8'),
            Nombre_Completo=data['Nombre_Completo'],
            Telefono=data['Telefono'],
            Direccion=data['Direccion'],
            Email=data['Email'],
            rol_id=data['rol_id'],
            activo=True,
            estado_verificacion='Pendiente'
        )

        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'message': 'Usuario creado exitosamente'}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# RUTAS COMPARTIDAS (AMBOS ROLES)

@app.route('/roles', methods=['GET'])
@token_requerido
def get_roles(usuario):
    roles = Rol.query.all()
    return jsonify([{'id': r.id, 'nombre': r.nombre} for r in roles])



# MAIN

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
