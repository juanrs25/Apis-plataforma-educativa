from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import db
from models import Inscripcion
from datetime import datetime
import requests
from correos_service.correo import enviar_correo

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

cache_usuarios = {}
cache_clases = {}
cache_profesor_clases = {}




#  1. CREAR SOLICITUD DE INSCRIPCIÓN

@app.route('/inscripciones', methods=['POST'])
def crear_inscripcion():
    data = request.get_json()

    id_usuario = data.get("id_usuario")
    id_clase = data.get("id_clase")

    # 1. Validar inscripción existente
    inscripcion = Inscripcion.query.filter_by(id_usuario=id_usuario, id_clase=id_clase).first()
    if inscripcion:
        return jsonify({
            "error": "Ya existe una inscripción",
            "estado_actual": inscripcion.estado
        }), 400

    # 2. Crear inscripción nueva
    nueva = Inscripcion(
        id_usuario=id_usuario,
        id_clase=id_clase,
        estado="Pendiente"
    )
    db.session.add(nueva)
    db.session.commit()

    # 3. Consultar usuario
    try:
        resp_user = requests.get(f"http://127.0.0.1:5001/usuarios-public/{id_usuario}")
        user_data = resp_user.json()
        nombre_cliente = user_data.get("Nombre_Completo")
        email_cliente = user_data.get("Email")
    except:
        nombre_cliente = "Usuario"
        email_cliente = None

    # 4. Consultar clase
    try:
        resp_clase = requests.get(f"http://127.0.0.1:5002/clases/{id_clase}")
        clase_data = resp_clase.json()
        nombre_clase = clase_data.get("titulo")
    except:
        nombre_clase = "Clase desconocida"

    # 5. Enviar correo llamando AL MICRO SERVICIO DE CORREOS
    if email_cliente:
        asunto = "Confirmación de inscripción"
        html = f"""
        <h2>Hola {nombre_cliente},</h2>
        <p>Te has registrado correctamente a la clase: <strong>{nombre_clase}</strong>.</p>
        <p>Tu solicitud está actualmente <strong>Pendiente</strong>.</p>
        <p>El profesor revisará tu inscripción.</p>
        <br>
        <p>Gracias,<br>Equipo Educando</p>
        """

        try:
            requests.post(
                "http://127.0.0.1:5005/enviar-correo",
                json={
                    "destinatario": email_cliente,
                    "asunto": asunto,
                    "html": html
                }
            )
        except Exception as e:
            print("Error llamando al servicio de correos:", e)

    return jsonify({
        "mensaje": "Inscripción creada y correo enviado",
        "estado": "Pendiente"
    }), 201



#  2. OBTENER SOLICITUDES DE INSCRIPCIÓN DE UN PROFESOR

@app.route('/inscripciones/profesor/<int:id_profesor>', methods=['GET'])
def solicitudes_por_profesor(id_profesor):

   
    # 1. Clases del profesor (cacheadas)
   
    if id_profesor not in cache_profesor_clases:
        try:
            resp = requests.get(f"http://localhost:5002/clases/profesor/{id_profesor}", timeout=2)
            cache_profesor_clases[id_profesor] = resp.json()
        except:
            return jsonify({"error": "No se pudo consultar las clases del profesor"}), 500

    clases_profesor = cache_profesor_clases[id_profesor]

    ids_clases = [c["clase"]["id_clase"] for c in clases_profesor]

   
    # 2. Inscripciones de esas clases
   
    solicitudes = Inscripcion.query.filter(
        Inscripcion.id_clase.in_(ids_clases)
    ).all()

    resultado = []

    for s in solicitudes:

    
        # 3. Usuario (cacheado)
        
        if s.id_usuario not in cache_usuarios:
            try:
                u = requests.get(f"http://localhost:5001/usuarios-public/{s.id_usuario}", timeout=2).json()
                cache_usuarios[s.id_usuario] = u
            except:
                cache_usuarios[s.id_usuario] = {"id": s.id_usuario, "Nombre_Completo": "Desconocido", "Email": None}

        usuario = cache_usuarios[s.id_usuario]

      
        # 4. Clase (cacheada)
   
        if s.id_clase not in cache_clases:
            try:
                c = requests.get(f"http://localhost:5002/clases/{s.id_clase}", timeout=2).json()
                cache_clases[s.id_clase] = c
            except:
                cache_clases[s.id_clase] = {"id_clase": s.id_clase, "titulo": "Desconocido", "horarios": []}

        clase = cache_clases[s.id_clase]

      
        # 5. Construcción final
        
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





# 3. ACEPTAR UNA INSCRIPCIÓN

@app.route('/inscripciones/<int:id_inscripcion>/aceptar', methods=['PUT'])
def aceptar(id_inscripcion):
    ins = Inscripcion.query.get(id_inscripcion)

    if not ins:
        return jsonify({"error": "Inscripción no encontrada"}), 404

    # Cambiar estado
    ins.estado = "Aprobada"
    db.session.commit()

   
    # 1. Obtener usuario
  
    try:
        resp_user = requests.get(f"http://127.0.0.1:5001/usuarios-public/{ins.id_usuario}")
        user_data = resp_user.json()
        nombre_cliente = user_data.get("Nombre_Completo")
        email_cliente = user_data.get("Email")
    except:
        nombre_cliente = "Usuario"
        email_cliente = None

  
    # 2. Obtener datos de la clase
 
    try:
        resp_clase = requests.get(f"http://127.0.0.1:5002/clases/{ins.id_clase}")
        clase_data = resp_clase.json()
        nombre_clase = clase_data.get("titulo")

        # Día de la clase
        dia = clase_data.get("horarios")[0].get("dia") if clase_data.get("horarios") else "día asignado"
    except:
        nombre_clase = "Clase desconocida"
        dia = "día asignado"

    # ------------------------------------------------
    # 3. ENVIAR CORREO DE ACEPTACIÓN
    # ------------------------------------------------
    if email_cliente:
        asunto = "Tu inscripción ha sido aprobada"
        html = f"""
        <h2>Hola {nombre_cliente},</h2>
        <p>Tu solicitud a la clase <strong>{nombre_clase}</strong> ha sido <strong>ACEPTADA</strong>.</p>
        <p>Nos vemos en los horarios correspondientes.</p>
        <br>
        <p>Gracias por elegirnos.<br>Equipo Educando</p>
        """

        try:
            requests.post(
                "http://127.0.0.1:5005/enviar-correo",
                json={
                    "destinatario": email_cliente,
                    "asunto": asunto,
                    "html": html
                }
            )
        except Exception as e:
            print("Error enviando correo de aceptación:", e)

    return jsonify({"mensaje": "Inscripción aprobada y correo enviado"}), 200





#  4. RECHAZAR UNA INSCRIPCIÓN (con envío de correo)

@app.route('/inscripciones/<int:id_inscripcion>/rechazar', methods=['PUT'])
def rechazar(id_inscripcion):
    ins = Inscripcion.query.get(id_inscripcion)

    if not ins:
        return jsonify({"error": "Inscripción no encontrada"}), 404

    # Cambiar estado
    ins.estado = "Rechazada"
    db.session.commit()

    
    # 1. Obtener usuario
    
    try:
        resp_user = requests.get(f"http://127.0.0.1:5001/usuarios-public/{ins.id_usuario}")
        user_data = resp_user.json()
        nombre_cliente = user_data.get("Nombre_Completo")
        email_cliente = user_data.get("Email")
    except:
        nombre_cliente = "Usuario"
        email_cliente = None

  
    # 2. Obtener datos del profesor
  
    try:
        resp_clase = requests.get(f"http://127.0.0.1:5002/clases/{ins.id_clase}")
        clase_data = resp_clase.json()

        nombre_clase = clase_data.get("titulo")

        # Datos del profesor
        profesor = clase_data.get("profesor", {})
        email_profesor = profesor.get("email", "No disponible")
    except:
        nombre_clase = "Clase desconocida"
        email_profesor = "No disponible"


    # 3. ENVIAR CORREO DE RECHAZO
  
    if email_cliente:
        asunto = "Tu inscripción ha sido rechazada"
        html = f"""
        <h2>Hola {nombre_cliente},</h2>
        <p>Tu solicitud a la clase <strong>{nombre_clase}</strong> ha sido <strong>RECHAZADA</strong>.</p>
        <p>Por favor comunícate con el correo del docente expuesto en la plataforma para más información.</p>
        <br>
        <p>Atentamente,<br>
        <strong>Equipo Educando</strong></p>
        """

        try:
            requests.post(
                "http://127.0.0.1:5005/enviar-correo",
                json={
                    "destinatario": email_cliente,
                    "asunto": asunto,
                    "html": html
                }
            )
        except Exception as e:
            print("Error enviando correo de rechazo:", e)

    return jsonify({"mensaje": "Inscripción rechazada y correo enviado"}), 200





#  5. OBTENER INSCRIPCIONES DE UN USUARIO

@app.route('/inscripciones/usuario/<int:id_usuario>', methods=['GET'])
def inscripciones_usuario(id_usuario):
    solicitudes = Inscripcion.query.filter_by(id_usuario=id_usuario).all()
    return jsonify([s.to_dict() for s in solicitudes]), 200



#  INICIO DEL SERVICIO

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5004, debug=True)
