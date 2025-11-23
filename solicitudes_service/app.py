from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from db import db
from models import Inscripcion
from datetime import datetime
import requests

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

cache_usuarios = {}
cache_clases = {}
cache_profesor_clases = {}



# -----------------------------------------------------------
#  1. CREAR SOLICITUD DE INSCRIPCIÓN
# -----------------------------------------------------------
@app.route('/inscripciones', methods=['POST'])
def crear_inscripcion():
    data = request.get_json()

    id_usuario = data.get("id_usuario")
    id_clase = data.get("id_clase")

    if not id_usuario or not id_clase:
        return jsonify({"error": "id_usuario e id_clase son obligatorios"}), 400

    #  Validar si ya existe inscripción previa
    existente = Inscripcion.query.filter_by(
        id_usuario=id_usuario,
        id_clase=id_clase
    ).first()

    if existente:
         if existente.estado == "Aprobada":
          return jsonify({
            "error": "Ya estás inscrito en esta clase",
            "estado_actual": "Aprobada"
        }), 409
         
         if existente.estado == "Pendiente":
          return jsonify({
            "error": "Ya enviaste una solicitud y está pendiente de aprobación",
            "estado_actual": "Pendiente"
        }), 409
         
         if existente.estado == "Rechazada":
          return jsonify({
            "error": "Tu solicitud fue rechazada. Consulta el correo del profesor.",
            "estado_actual": "Rechazada"
        }), 409
    #  Validar usuario en API de usuarios
    try:
        resp_usr = requests.get(f"http://localhost:5001/usuarios-public/{id_usuario}")
        if resp_usr.status_code != 200:
            return jsonify({"error": "El usuario no existe"}), 404
    except:
        return jsonify({"error": "No se pudo conectar a usuarios"}), 500

    # Validar clase en API de clases
    try:
        resp_cls = requests.get(f"http://localhost:5002/clases/{id_clase}")
        if resp_cls.status_code != 200:
            return jsonify({"error": "La clase no existe"}), 404
    except:
        return jsonify({"error": "No se pudo conectar al servicio de clases"}), 500

    #  Crear la nueva inscripción
    nueva = Inscripcion(
        id_usuario=id_usuario,
        id_clase=id_clase,
        estado="Pendiente",
        fecha_inscripcion=datetime.now()
    )

    db.session.add(nueva)
    db.session.commit()

    return jsonify({
        "mensaje": "Solicitud enviada correctamente",
        "inscripcion": nueva.to_dict()
    }), 201




# -----------------------------------------------------------e
#  2. OBTENER SOLICITUDES DE INSCRIPCIÓN DE UN PROFESOR
# -----------------------------------------------------------
@app.route('/inscripciones/profesor/<int:id_profesor>', methods=['GET'])
def solicitudes_por_profesor(id_profesor):

    # --------------------------------------------
    # 1. Clases del profesor (cacheadas)
    # --------------------------------------------
    if id_profesor not in cache_profesor_clases:
        try:
            resp = requests.get(f"http://localhost:5002/clases/profesor/{id_profesor}", timeout=2)
            cache_profesor_clases[id_profesor] = resp.json()
        except:
            return jsonify({"error": "No se pudo consultar las clases del profesor"}), 500

    clases_profesor = cache_profesor_clases[id_profesor]

    ids_clases = [c["clase"]["id_clase"] for c in clases_profesor]

    # --------------------------------------------
    # 2. Inscripciones de esas clases
    # --------------------------------------------
    solicitudes = Inscripcion.query.filter(
        Inscripcion.id_clase.in_(ids_clases)
    ).all()

    resultado = []

    for s in solicitudes:

        # --------------------------------------------
        # 3. Usuario (cacheado)
        # --------------------------------------------
        if s.id_usuario not in cache_usuarios:
            try:
                u = requests.get(f"http://localhost:5001/usuarios-public/{s.id_usuario}", timeout=2).json()
                cache_usuarios[s.id_usuario] = u
            except:
                cache_usuarios[s.id_usuario] = {"id": s.id_usuario, "Nombre_Completo": "Desconocido", "Email": None}

        usuario = cache_usuarios[s.id_usuario]

        # --------------------------------------------
        # 4. Clase (cacheada)
        # --------------------------------------------
        if s.id_clase not in cache_clases:
            try:
                c = requests.get(f"http://localhost:5002/clases/{s.id_clase}", timeout=2).json()
                cache_clases[s.id_clase] = c
            except:
                cache_clases[s.id_clase] = {"id_clase": s.id_clase, "titulo": "Desconocido", "horarios": []}

        clase = cache_clases[s.id_clase]

        # --------------------------------------------
        # 5. Construcción final
        # --------------------------------------------
        resultado.append({
            "id_inscripcion": s.id_inscripcion,
            "estado": s.estado,
            "fecha_inscripcion": s.fecha_inscripcion.strftime("%Y-%m-%d %H:%M:%S"),

            "usuario": {
                "id_usuario": usuario.get("id"),
                "nombre": usuario.get("Nombre_Completo"),
                "email": usuario.get("Email")
            },

            "clase": {
                "id_clase": clase.get("id_clase"),
                "nombre_clase": clase.get("titulo"),
                "dia": clase.get("horarios")[0].get("dia") if clase.get("horarios") else None  
            }
        })

    return jsonify(resultado), 200




# -----------------------------------------------------------
# 🔵 3. ACEPTAR UNA INSCRIPCIÓN
# -----------------------------------------------------------
@app.route('/inscripciones/<int:id_inscripcion>/aceptar', methods=['PUT'])
def aceptar(id_inscripcion):
    ins = Inscripcion.query.get(id_inscripcion)

    if not ins:
        return jsonify({"error": "Inscripción no encontrada"}), 404

    ins.estado = "Aprobada"
    db.session.commit()

    return jsonify({"mensaje": "Inscripción aprobada", "inscripcion": ins.to_dict()}), 200



# -----------------------------------------------------------
# 🔵 4. RECHAZAR UNA INSCRIPCIÓN
# -----------------------------------------------------------
@app.route('/inscripciones/<int:id_inscripcion>/rechazar', methods=['PUT'])
def rechazar(id_inscripcion):
    ins = Inscripcion.query.get(id_inscripcion)

    if not ins:
        return jsonify({"error": "Inscripción no encontrada"}), 404

    ins.estado = "Rechazada"
    db.session.commit()

    return jsonify({"mensaje": "Inscripción rechazada", "inscripcion": ins.to_dict()}), 200



# -----------------------------------------------------------
# 🔵 5. OBTENER INSCRIPCIONES DE UN USUARIO
# -----------------------------------------------------------
@app.route('/inscripciones/usuario/<int:id_usuario>', methods=['GET'])
def inscripciones_usuario(id_usuario):
    solicitudes = Inscripcion.query.filter_by(id_usuario=id_usuario).all()
    return jsonify([s.to_dict() for s in solicitudes]), 200


# -----------------------------------------------------------
# 🔵 INICIO DEL SERVICIO
# -----------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5004, debug=True)
