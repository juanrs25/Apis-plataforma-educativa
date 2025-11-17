import datetime
from flask import Flask, jsonify, request
from config import Config
from db import db
from models import Clase, Horario
import requests
from datetime import datetime
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

# CREAR UNA CLASE (y su horario al mismo tiempo)
@app.route('/clases', methods=['POST'])
def crear_clase():
    data = request.get_json()

    # Validación de campos requeridos
    if not data.get('titulo') or not data.get('profesor_id') or not data.get('dia'):
        return jsonify({"error": "Faltan campos obligatorios (titulo, profesor_id o dia)"}), 400

    profesor_id = data['profesor_id']
    dia = data['dia']

    # Verificar que el profesor exista en la API de usuarios
    try:
        resp = requests.get(f'http://localhost:5001/usuarios/{profesor_id}', timeout=3)
        if resp.status_code != 200:
            return jsonify({"error": "El profesor no existe"}), 400
    except requests.exceptions.RequestException:
        return jsonify({"error": "No se pudo conectar con el servicio de usuarios"}), 500

    # Crear la clase
    nueva_clase = Clase(
        titulo=data['titulo'],
        descripcion=data.get('descripcion'),
        profesor_id=profesor_id,
        precio=data.get('precio'),
        estado=data.get('estado', 'Activa'),
        fecha_creacion=datetime.now()
    )

    db.session.add(nueva_clase)
    db.session.commit()

    # Crear horario automáticamente
    nuevo_horario = Horario(
        id_clase=nueva_clase.id_clase,
        dia=dia
    )
    db.session.add(nuevo_horario)
    db.session.commit()

    return jsonify({
        "mensaje": "Clase y horario creados exitosamente",
        "clase": nueva_clase.to_dict(),
        "horario": nuevo_horario.to_dict()
    }), 201



#  OBTENER CLASES POR PROFESOR
@app.route('/clases/profesor/<int:profesor_id>', methods=['GET'])
def obtener_clases_de_profesor(profesor_id):
    clases = Clase.query.filter_by(profesor_id=profesor_id).all()

    resultado = []
    for c in clases:
        horarios = Horario.query.filter_by(id_clase=c.id_clase).all()
        resultado.append({
            "clase": c.to_dict(),
            "horarios": [h.to_dict() for h in horarios]
        })

    return jsonify(resultado), 200


# ACTUALIZAR UNA CLASE
@app.route('/clases/<int:id_clase>', methods=['PUT'])
def actualizar_clase(id_clase):
    clase = Clase.query.get(id_clase)
    if not clase:
        return jsonify({"error": "Clase no encontrada"}), 404

    data = request.get_json()

    # Actualizar solo los campos enviados
    clase.titulo = data.get('titulo', clase.titulo)
    clase.descripcion = data.get('descripcion', clase.descripcion)
    clase.precio = data.get('precio', clase.precio)
    clase.estado = data.get('estado', clase.estado)

    db.session.commit()
    return jsonify({"mensaje": "Clase actualizada correctamente", "clase": clase.to_dict()}), 200


#  ELIMINAR UNA CLASE (también borra su horario)
@app.route('/clases/<int:id_clase>', methods=['DELETE'])
def eliminar_clase(id_clase):
    clase = Clase.query.get(id_clase)
    if not clase:
        return jsonify({"error": "Clase no encontrada"}), 404

    # Eliminar horarios asociados
    Horario.query.filter_by(id_clase=id_clase).delete()

    db.session.delete(clase)
    db.session.commit()
    return jsonify({"mensaje": "Clase y su horario eliminados correctamente"}), 200


#  LISTAR TODAS LAS CLASES
@app.route('/clases', methods=['GET'])
def listar_clases():
    clases = Clase.query.all()
    resultado = []
    for c in clases:
        horarios = Horario.query.filter_by(id_clase=c.id_clase).all()
        resultado.append({
            "clase": c.to_dict(),
            "horarios": [h.to_dict() for h in horarios]
        })
    return jsonify(resultado), 200

# INICIO DEL SERVICIO
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5002, debug=True)
