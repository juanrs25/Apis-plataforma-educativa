from flask import Flask, jsonify, request
from config import Config
from db import db
from models import Clase
import requests

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# --------------------------
# CREAR UNA CLASE
# --------------------------
@app.route('/clases', methods=['POST'])
def crear_clase():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('titulo') or not data.get('profesor_id'):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    profesor_id = data['profesor_id']

    # Consultar API de usuarios para verificar que el profesor existe
    try:
        resp = requests.get(f'http://localhost:5001/usuarios/{profesor_id}', timeout=3)
        if resp.status_code != 200:

            
            return jsonify({"error": "El profesor no existe"}), 400
    except requests.exceptions.RequestException:
        return jsonify({"error": "No se pudo conectar con el servicio de usuarios"}), 500

    nueva_clase = Clase(
        titulo=data['titulo'],
        descripcion=data.get('descripcion'),
        profesor_id=profesor_id,
        precio=data.get('precio'),
        estado=data.get('estado', 'Activa')
    )

    db.session.add(nueva_clase)
    db.session.commit()

    return jsonify({"mensaje": "Clase creada exitosamente"}), 201


# --------------------------
# LISTAR TODAS LAS CLASES
# --------------------------
@app.route('/clases', methods=['GET'])
def listar_clases():
    clases = Clase.query.all()
    resultado = [c.to_dict() for c in clases]
    return jsonify(resultado), 200


# --------------------------
# OBTENER UNA CLASE POR ID
# --------------------------
@app.route('/clases/<int:id_clase>', methods=['GET'])
def obtener_clase(id_clase):
    clase = Clase.query.get(id_clase)
    if not clase:
        return jsonify({"error": "Clase no encontrada"}), 404
    return jsonify(clase.to_dict()), 200


# --------------------------
# ACTUALIZAR UNA CLASE
# --------------------------
@app.route('/clases/<int:id_clase>', methods=['PUT'])
def actualizar_clase(id_clase):
    clase = Clase.query.get(id_clase)
    if not clase:
        return jsonify({"error": "Clase no encontrada"}), 404

    data = request.get_json()
    clase.titulo = data.get('titulo', clase.titulo)
    clase.descripcion = data.get('descripcion', clase.descripcion)
    clase.precio = data.get('precio', clase.precio)
    clase.estado = data.get('estado', clase.estado)

    db.session.commit()
    return jsonify({"mensaje": "Clase actualizada correctamente"}), 200


# --------------------------
# ELIMINAR UNA CLASE
# --------------------------
@app.route('/clases/<int:id_clase>', methods=['DELETE'])
def eliminar_clase(id_clase):
    clase = Clase.query.get(id_clase)
    if not clase:
        return jsonify({"error": "Clase no encontrada"}), 404

    db.session.delete(clase)
    db.session.commit()
    return jsonify({"mensaje": "Clase eliminada correctamente"}), 200


# --------------------------
# INICIO DEL SERVICIO
# --------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5002, debug=True)
