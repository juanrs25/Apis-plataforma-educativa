from flask import Flask, jsonify, request
from flask_cors import CORS
from db import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from models import Usuario, Rol
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps


# CONFIGURACIÓN FLASK------------------
app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)

# HELPERS---------------

#Genera un JWT válido por 'horas' horas"
def generar_token(usuario, horas=2):
    return jwt.encode({
        'id': usuario.id,
        'rol': usuario.rol.nombre,
        'exp': datetime.utcnow() + timedelta(hours=horas)
    }, SECRET_KEY, algorithm='HS256')

def crear_usuario(data, rol_id, activo=True, estado='Aprobado'):
    """Crea un objeto Usuario con contraseña encriptada"""
    hashed = bcrypt.hashpw(data['Clave'].encode('utf-8'), bcrypt.gensalt())
    return Usuario(
        Usuario=data['Usuario'],
        Clave=hashed.decode('utf-8'),
        Nombre_Completo=data['Nombre_Completo'],
        Telefono=data.get('Telefono'),
        Direccion=data.get('Direccion'),
        Email=data.get('Email'),
        rol_id=rol_id,
        activo=activo,
        estado_verificacion=estado
    )

# DECORADORES----------------------------------------

 #Verifica que exista un token JWT válido y que el usuario esté activo"""
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
                token = parts[0]

        if not token:
            return jsonify({'mensaje': 'Necesitas token para acceder a esta ruta'}), 401

        try:
            #  Decodificar y validar el token (verifica exp automáticamente)
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            usuario_actual = Usuario.query.filter_by(id=data['id']).first()
            if not usuario_actual:
                return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        except jwt.ExpiredSignatureError:
            #  Si el token expiró
            return jsonify({'mensaje': 'El token ha expirado, por favor inicia sesión nuevamente.'}), 401

        except jwt.InvalidTokenError:
            #  Si el token no es válido
            return jsonify({'mensaje': 'Token inválido.'}), 401

        return f(usuario_actual, *args, **kwargs)
    return decorated

# """Verifica que el usuario autenticado sea administrador"""
def solo_admin(f):
    @wraps(f)
    def decorated(usuario, *args, **kwargs):
        if usuario.rol.nombre != 'Admin':
            return jsonify({'message': 'Solo administradores pueden realizar esta acción'}), 403
        return f(usuario, *args, **kwargs)
    return decorated


# RUTAS PÚBLICAS---------------------------------------------------------------------------------

@app.route('/')
def index():
    return jsonify({"message": "API Usuarios corriendo con MySQL"})

# """Registro público para Cliente (activo) o Profesor (pendiente)"""--------------------------------
@app.route('/registro', methods=['POST'])
def registro_publico():
    data = request.get_json()
    rol_id = data.get('rol_id')

    try:
        # Convertimos a entero (y manejamos el caso si no llega)
        rol_id = int(data.get('rol_id', 0))
    except (ValueError, TypeError):
        return jsonify({'message': 'Rol inválido'}), 400

    print(f"✅ Rol procesado como entero: {rol_id} ({type(rol_id)})")

    if rol_id not in [2, 3]:
        return jsonify({'message': 'Rol inválido para registro público'}), 400

    usuario = crear_usuario(
        data,
        rol_id=rol_id,
        activo=(rol_id==2),
        estado='Aprobado' if rol_id==2 else 'Pendiente'
    )
    db.session.add(usuario)
    db.session.commit()

    mensaje = 'Cliente registrado exitosamente' if rol_id==2 else 'Profesor registrado, pendiente de aprobación por admin'
    return jsonify({'message': mensaje}), 201

@app.route('/login', methods=['POST'])
# """Login de usuario, solo activos pueden iniciar sesión"""-----------------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(Usuario=data['Usuario']).first()

    if not usuario:
        return jsonify({'message': 'Credenciales invalidas'}), 404

    if not bcrypt.checkpw(data['Clave'].encode('utf-8'), usuario.Clave.encode('utf-8')):
        return jsonify({'message': 'Credenciales invalidas'}), 401

    # Tiempo de expiración del token: 5 minutos
    exp_time = datetime.utcnow() + timedelta(minutes=1)

    token = jwt.encode({
        'id': usuario.id,
        'rol': usuario.rol.nombre,
        'exp': exp_time
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'message': 'Inicio de sesión exitoso',
        'token': token,
        'rol': usuario.rol.nombre,
         'nombre': usuario.Nombre_Completo,
        'expira_en': exp_time.isoformat() + 'Z'  # Muestra cuándo expira
        
    }), 200

# ENDPOINT PUBLICO PARA MICRO-SERVICIOS (NO REQUIERE TOKEN)
@app.route('/usuarios-public/<int:id_usuario>', methods=['GET'])
def usuario_public(id_usuario):
    user = Usuario.query.get(id_usuario)
    if not user:
        return jsonify({'existe': False}), 404

    return jsonify({
        'existe': True,
        'id': user.id,
        'activo': user.activo,
        'rol': user.rol.nombre if user.rol else None
    }), 200


# RUTAS ADMIN---------------------------------------------------------------------------------------
#OBTENER USUARIO POR ID
@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
@token_requerido
def obtener_usuario(id_usuario):
    user = Usuario.query.get(id_usuario)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({
        'id': user.id,
        'Usuario': user.Usuario,
        'Nombre_Completo': user.Nombre_Completo,
        'Email': user.Email,
        'rol': user.rol.nombre if user.rol else None,
        'activo': user.activo
    }), 200

#Funcion para listar todos los usuarios
@app.route('/usuarios', methods=['GET'])
@token_requerido
def get_usuarios(usuario):
    # Si el usuario es ADMIN: puede ver todos los usuarios
    if usuario.rol.nombre == 'Admin':
        usuarios = Usuario.query.all()

    # Si el usuario es CLIENTE: solo puede ver usuarios con rol DOCENTE
    elif usuario.rol.nombre == 'Cliente':
        usuarios = Usuario.query.join(Rol).filter(Rol.nombre == 'Docente').all()
    #Si el usuario es DOCENTE: solo puede ver a los usuarios registrados como clientes

    elif usuario.rol.nombre == 'Docente':
        usuarios = Usuario.query.join(Rol).filter(Rol.nombre == 'Cliente').all()

    else:
        return jsonify({'message': 'No tienes permisos para acceder a esta ruta'}), 403

    # Formato de salida
    return jsonify([{
        'Usuario': u.Usuario,
        'Nombre_Completo': u.Nombre_Completo,
        'Email': u.Email,
        'Telefono':u.Telefono,
        'rol': u.rol.nombre if u.rol else None,
        
    } for u in usuarios]), 200
            
#--------------------------------------------------------------------------------------------------------------------------
# ACTUALIZAR USUARIO (solo Admin)
@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
@token_requerido
def actualizar_usuario(usuario, id_usuario):
    # Solo el administrador puede actualizar usuarios
    if usuario.rol.nombre != 'Admin':
        return jsonify({'message': 'Solo los administradores pueden actualizar usuarios.'}), 403

    user = Usuario.query.get(id_usuario)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json()

    # Actualizar solo los campos que lleguen en la petición
    user.Nombre_Completo = data.get('Nombre_Completo', user.Nombre_Completo)
    user.Email = data.get('Email', user.Email)
    user.Telefono = data.get('Telefono', user.Telefono)
    user.Direccion = data.get('Direccion', user.Direccion)
    
    # Permitir cambiar el rol (si llega)
    if 'rol' in data:
        nuevo_rol = Rol.query.filter_by(nombre=data['rol']).first()
        if nuevo_rol:
            user.rol_id = nuevo_rol.id
        else:
            return jsonify({'error': 'Rol no válido'}), 400

    db.session.commit()
    return jsonify({'message': f'Usuario {user.Usuario} actualizado correctamente.'}), 200


# ELIMINAR USUARIO (solo Admin)-------------------------------------------------------------------------------------
@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
@token_requerido
def eliminar_usuario(usuario, id_usuario):
    # Solo el administrador puede eliminar usuarios
    if usuario.rol.nombre != 'Admin':
        return jsonify({'message': 'Solo los administradores pueden eliminar usuarios.'}), 403

    user = Usuario.query.get(id_usuario)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'Usuario {user.Usuario} eliminado correctamente.'}), 200

#"""Aprovacion de un Docente pendiente"""------------------------------------------------------------------------------
@app.route('/usuarios/aprobar/<int:id_usuario>', methods=['PUT'])
@token_requerido
@solo_admin
def aprobar_profesor(usuario, id_usuario):
    u = Usuario.query.get(id_usuario)
    if not u: return jsonify({'message': 'Usuario no encontrado'}), 404
    if u.rol.nombre != 'Docente': return jsonify({'message': 'Solo se pueden aprobar profesores'}), 400
    u.activo = True
    u.estado_verificacion = 'Aprobado'
    db.session.commit()
    return jsonify({'message': f'Docente {u.Usuario} aprobado exitosamente'})

 #"""Crear admin o profesor directamente (solo admin)"""----------------------------------------------------
@app.route('/usuarios', methods=['POST'])
@token_requerido
@solo_admin
def crear_usuario_admin(usuario):
    data = request.get_json()
    usuario_nuevo = crear_usuario(data, rol_id=data['rol_id'], activo=True, estado='Aprobado')
    db.session.add(usuario_nuevo)
    db.session.commit()
    return jsonify({'message': 'Usuario creado exitosamente'}), 201

# RUTAS COMPARTIDAS-------------------------------------------------
@app.route('/roles', methods=['GET'])
@token_requerido
@solo_admin
def get_roles(usuario):
    """Listar todos los roles disponibles"""
    return jsonify([{'id': r.id, 'nombre': r.nombre} for r in Rol.query.all()])

# MAIN
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
