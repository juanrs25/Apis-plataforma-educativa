from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


# CONFIGURACIÓN BREVO

BREVO_API_KEY = "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"  
BREVO_URL = "https://api.brevo.com/v3/smtp/email"



# FUNCIÓN PARA ENVIAR CORREO

def enviar_correo(destinatario, asunto, html):
    try:
        payload = {
            "sender": {
                "name": "Educando",
                "email": "rodsil2209@gmail.com"  
            },
            "to": [
                {"email": destinatario}
            ],
            "subject": asunto,
            "htmlContent": html
        }

        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }

        response = requests.post(BREVO_URL, json=payload, headers=headers)

        if response.status_code in [200, 201]:
            print("Correo enviado correctamente:", response.json())
            return True, response.json()
        else:
            print("Error:", response.text)
            return False, response.text

    except Exception as e:
        print("Error general:", e)
        return False, str(e)



# ENDPOINT PÚBLICO

@app.route('/enviar-correo', methods=['POST'])
def enviar():
    data = request.get_json()

    destinatario = data.get("destinatario")
    asunto = data.get("asunto")
    html = data.get("html")

    if not destinatario or not asunto or not html:
        return jsonify({"error": "Faltan parámetros"}), 400

    ok, resp = enviar_correo(destinatario, asunto, html)

    if ok:
        return jsonify({
            "mensaje": "Correo enviado correctamente",
            "detalle": resp
        }), 200
    else:
        return jsonify({
            "error": "No se pudo enviar el correo",
            "detalle": resp
        }), 500



# INICIO DEL SERVICIO

if __name__ == '__main__':
    print("Servicio de correos activo en http://127.0.0.1:5005 ...")
    app.run(port=5005, debug=True)
