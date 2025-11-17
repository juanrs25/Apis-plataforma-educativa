from wsgiref.simple_server import make_server
from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from service import PQRService  # Tu servicio SOAP

# 1. Target Namespace (debe ser único)
APP_TNS = "spyne.servicio.pqrs"

# 2. Aplicación Spyne
application = Application(
    [PQRService],                        
    tns=APP_TNS,                         
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11()                
)


wsgi_application = WsgiApplication(application)

# 4. Iniciar servidor
if __name__ == "__main__":
    server_address = "127.0.0.1"
    server_port = 5003   
    
    server = make_server(server_address, server_port, wsgi_application)

    print(f"Servidor SOAP PQRS corriendo en http://{server_address}:{server_port}")
    print(f"WSDL disponible en: http://{server_address}:{server_port}/?wsdl")

    server.serve_forever()
