import os

# --- Configuración de la base de datos MySQL ---
USERNAME = os.getenv('DB_USER', 'root')            # Usuario de MySQL
PASSWORD = os.getenv('DB_PASS', '')                # Contraseña (vacía si no tiene)
HOST = os.getenv('DB_HOST', 'localhost')           # Servidor (localhost por defecto)
DATABASE = os.getenv('DB_NAME', 'plataformaeducativa')  # Nombre de la base de datos

# URI de conexión (maneja correctamente si la contraseña está vacía)
if PASSWORD:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}?charset=utf8mb4'
else:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}@{HOST}/{DATABASE}?charset=utf8mb4'

# --- Otras configuraciones ---
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')  # Usa variable de entorno o valor por defecto
