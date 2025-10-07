import os

class Config:
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASS = os.getenv('DB_PASS', '')           # deja vacío por defecto si no hay contraseña
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'basedos')

    # Construye la URI de forma segura si la contraseña está vacía
    if DB_PASS:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    else:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SECRET_KEY: preferible tomarla de una variable de entorno en producción
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-para-desarrollo'
