from flask import Flask, jsonify, request
from flask_cors import CORS
from db import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import Usuario, Rol
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

# ✅ Ruta de prueba
@app.route('/')
def index():
    return jsonify({"message": "API Usuarios corriendo con MySQL"})

# ✅ Obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        'id': u.id,
        'Usuario': u.Usuario,
        'Nombre_Completo': u.Nombre_Completo,
        'Email': u.Email,
        'rol': u.rol.nombre if u.rol else None,
        'estado_verificacion': u.estado_verificacion
    } for u in usuarios])


# ✅ Obtener un usuario por ID
@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        'id': usuario.id,
        'Usuario': usuario.Usuario,
        'Nombre_Completo': usuario.Nombre_Completo,
        'Email': usuario.Email,
        'rol': usuario.rol.nombre if usuario.rol else None,
        'estado_verificacion': usuario.estado_verificacion
    }), 200


# ✅ Obtener todos los roles
@app.route('/roles', methods=['GET'])
def get_roles():
    roles = Rol.query.all()
    return jsonify([{
        'id': r.id,
        'nombre': r.nombre
    } for r in roles])


# ✅ Crear usuario (POST) — Cliente o Docente
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    try:
        data = request.get_json()

        tipo_usuario = data.get('tipo_usuario', 'Cliente')  # viene del formulario
        CAMPOS_CLIENTE = ['Usuario', 'Clave', 'Nombre_Completo', 'Telefono', 'Direccion', 'Email', 'rol_id']
        CAMPOS_DOCENTE = CAMPOS_CLIENTE + ['Experiencia', 'Titulo_Profesional', 'Hoja_de_Vida']

        # Verificar campos requeridos
        campos_requeridos = CAMPOS_DOCENTE if tipo_usuario == 'Docente' else CAMPOS_CLIENTE
        faltantes = [campo for campo in campos_requeridos if campo not in data and campo not in request.files]
        if faltantes:
            return jsonify({"error": f"Faltan los campos: {', '.join(faltantes)}"}), 400

        # Crear objeto Usuario
        nuevo = Usuario(
            Usuario=data['Usuario'],
            Clave=data['Clave'],
            Nombre_Completo=data['Nombre_Completo'],
            Telefono=data['Telefono'],
            Direccion=data['Direccion'],
            Email=data['Email'],
            rol_id=data['rol_id'],
            activo=True,
            experiencia_laboral=data.get('Experiencia'),
            titulo_profesional=data.get('Titulo_Profesional'),
            estado_verificacion='Pendiente'
        )

        # Guardar hoja de vida (si aplica)
        if tipo_usuario == 'Docente' and 'Hoja_de_Vida' in request.files:
            archivo = request.files['Hoja_de_Vida']
            if archivo.filename != '':
                ruta_archivo = os.path.join('uploads', archivo.filename)
                archivo.save(ruta_archivo)
                nuevo.hoja_vida_path = ruta_archivo

        db.session.add(nuevo)
        db.session.commit()

        return jsonify({'message': 'Usuario creado exitosamente'}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
