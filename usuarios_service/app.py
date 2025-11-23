from flask import Flask, jsonify, request
from flask_cors import CORS
from db import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from models import Usuario, Rol
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os

# CONFIGURACIÓN FLASK------------------
app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)

# HELPERS---------------
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
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
        estado_verificacion=estado,
        experiencia_laboral=data.get('experiencia_laboral'),
        hoja_vida_path=data.get('hoja_vida_path'),
        titulo_profesional=data.get('titulo_profesional')
    )



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
#................................................................#
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

# """Registro público para Cliente (activo) o Profesor (pendiente)
@app.route('/registro', methods=['POST'])
def registro_publico():

    # Datos normales del formulario
    data = request.form.to_dict()

    # Archivo PDF
    archivo = request.files.get('hoja_vida_path')

    # Rol
    rol_id = data.get('rol_id')

    try:
        rol_id = int(rol_id)
    except (ValueError, TypeError):
        return jsonify({'message': 'Rol inválido'}), 400

    print(f"✅ Rol recibido: {rol_id}")

    if rol_id not in [2, 3]:
        return jsonify({'message': 'Rol inválido para registro público'}), 400

    # Si es profesor (rol 3), debe subir PDF
    if rol_id == 3:
        if not archivo:
            return jsonify({'message': 'Debe subir la hoja de vida'}), 400
        
        # Guardar archivo en uploads
        filename = archivo.filename
        archivo.save(os.path.join(UPLOAD_FOLDER, filename))
        print("📄 Archivo guardado correctamente:", filename)

        # Se guarda solo el nombre del archivo
        data['hoja_vida_path'] = filename

    # Crear usuario
    usuario = crear_usuario(
        data,
        rol_id=rol_id,
        activo=(rol_id == 2),
        estado='Aprobado' if rol_id == 2 else 'Pendiente'
    )
    db.session.add(usuario)
    db.session.commit()

    mensaje = (
        'Cliente registrado exitosamente'
        if rol_id == 2
        else 'Profesor registrado, pendiente de aprobación por admin'
    )

    return jsonify({'message': mensaje}), 201


# """Login de usuario, solo activos pueden iniciar sesión"""-----------------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(Usuario=data['Usuario']).first()

    if not usuario:
        return jsonify({'message': 'Credenciales invalidas'}), 404

    if not bcrypt.checkpw(data['Clave'].encode('utf-8'), usuario.Clave.encode('utf-8')):
        return jsonify({'message': 'Credenciales invalidas'}), 401
     #Validar si es docente y aún no está aprobado
    if usuario.rol_id == 3 and usuario.estado_verificacion.lower() != "aprobado":
        return jsonify({
            'message': 'Tu cuenta está pendiente de aprobación por el administrador.'
        }), 403
    # Tiempo de expiración del token: 60 minutos
    exp_time = datetime.utcnow() + timedelta(minutes=60)

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
        #'activo': user.activo,
        'rol': user.rol.nombre if user.rol else None,
        'Nombre_Completo': user.Nombre_Completo,
        'Email': user.Email,

        
    }), 200


# RUTAS ADMIN---------------------------------------------------------------------------------------
#................................................................................................................#
@app.route('/usuarios/todos', methods=['GET'])
@token_requerido
@solo_admin
def obtener_todos(usuario):
    usuarios = Usuario.query.all()

    lista = []
    for u in usuarios:
        lista.append({
            "id": u.id,
            "nombre": u.Nombre_Completo,
            "email": u.Usuario,
            "rol": u.rol.nombre,
            "estado": u.estado_verificacion,
            "activo": u.activo,
            "hoja_vida": u.hoja_vida_path
        })

    return jsonify(lista), 200
#.......................Activar usuario...................................#
@app.route('/usuarios/activar/<int:id_usuario>', methods=['PUT'])
@token_requerido
@solo_admin
def activar_usuario(usuario, id_usuario):
    u = Usuario.query.get(id_usuario)

    if not u:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    u.activo = True
    u.estado_verificacion = "Aprobado"
    db.session.commit()

    return jsonify({'message': 'Usuario activado'}), 200
#.........................Desactivar usuario..................................#
@app.route('/usuarios/desactivar/<int:id_usuario>', methods=['PUT'])
@token_requerido
@solo_admin
def desactivar_usuario(usuario, id_usuario):
    u = Usuario.query.get(id_usuario)

    if not u:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    u.activo = False
    db.session.commit()

    return jsonify({'message': 'Usuario desactivado'}), 200
#.....................................................................................#
#OBTENER USUARIO POR ID
@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
@token_requerido
def obtener_usuario(usuario, id_usuario):

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
#................................................................................................................#
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

#................................................................................................................#
#funcion para listar todos los docentes activos
@app.route('/docentes', methods=['GET'])
def listar_docentes(usuario):
    docentes = Usuario.query.join(Rol).filter(
        Rol.nombre == 'Docente',
        Usuario.activo == True
    ).all()

    return jsonify({
        "usuarios": [{
            "id_usuario": d.id,
            "nombre": d.Nombre_Completo,
            "correo": d.Email,
            "telefono": d.Telefono,
            "foto": None,  # puedes cambiarlo si agregas foto
            "titulo": d.titulo_profesional,
            "experiencia": d.experiencia_laboral
        } for d in docentes]
    }), 200     
#................................................................................................................#
#"Listar docentes pendientes de aprobación (solo Admin)"
@app.route('/usuarios/pendientes', methods=['GET'])
@token_requerido
@solo_admin
def docentes_pendientes(usuario):
    docentes = Usuario.query.filter_by(rol_id=3, activo=False).all()

    resultado = []
    for d in docentes:
        resultado.append({
            "id": d.id,
            "nombre": d.Nombre_Completo,
            "email": d.Email,
            "estado": d.estado_verificacion,
            "hoja_vida_path": d.hoja_vida_path
        })
    
    return jsonify(resultado), 200
#................................................................................................................#
#"Rechazar la aprobación de un Docente pendiente (solo Admin)"
@app.route('/usuarios/rechazar/<int:id_usuario>', methods=['PUT'])
@token_requerido
@solo_admin
def rechazar_profesor(usuario, id_usuario):
    u = Usuario.query.get(id_usuario)
    if not u: 
        return jsonify({'message': 'Usuario no encontrado'}), 404
    if u.rol.nombre != 'Docente': 
        return jsonify({'message': 'Solo se pueden rechazar profesores'}), 400

    u.activo = False
    u.estado_verificacion = 'Rechazado'
    db.session.commit()

    return jsonify({'message': f'Docente {u.Usuario} rechazado exitosamente'})
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
#..................................................................................................................#
from flask import send_from_directory
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('./uploads', filename)

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
