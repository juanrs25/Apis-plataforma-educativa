from app import app
from db import db

# Importar tus modelos para que SQLAlchemy los reconozca
from models import *

with app.app_context():
    print("📦 Creando base de datos usuarios.db ...")
    db.create_all()
    print("✅ Base de datos creada correctamente.")
