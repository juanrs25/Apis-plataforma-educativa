from wsgiref.simple_server import make_server
from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from service import PQRService  # Tu servicio SOAP

# 1. Target Namespace (debe ser único)
APP_TNS = "spyne.servicio.pqrs"

# 2. Aplicación Spyne
application = Application(
    [PQRService],                        # Lista de servicios
    tns=APP_TNS,                         # Namespace del servicio
    in_protocol=Soap11(validator="lxml"),# SOAP 1.1 entrada
    out_protocol=Soap11()                # SOAP 1.1 salida
)

# 3. Crear la aplicación WSGI
wsgi_application = WsgiApplication(application)

# 4. Iniciar servidor
if __name__ == "__main__":
    server_address = "127.0.0.1"
    server_port = 5003   # Puedes dejarlo como otro microservicio
    
    server = make_server(server_address, server_port, wsgi_application)

    print(f"Servidor SOAP PQRS corriendo en http://{server_address}:{server_port}")
    print(f"WSDL disponible en: http://{server_address}:{server_port}/?wsdl")

    server.serve_forever()
