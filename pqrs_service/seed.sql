-- Crear base de datos
CREATE DATABASE IF NOT EXISTS pqrs_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE pqrs_db;

-- Crear tabla pqrs
CREATE TABLE IF NOT EXISTS pqrs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    asunto VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_creacion DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
