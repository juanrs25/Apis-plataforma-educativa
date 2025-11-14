import os

class Config:
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASS = os.getenv('DB_PASS', '')           # deja vacío por defecto si no hay contraseña
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'db_pqrs')

    # URI de SQLAlchemy
    if DB_PASS:
        DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    else:
        DATABASE_URL = f"mysql+pymysql://{DB_USER}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"

    # Clave secreta (por si más adelante quieres autenticar algo)
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-para-desarrollo'
