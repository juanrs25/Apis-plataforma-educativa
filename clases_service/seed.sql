-- =========================================================
-- SCRIPT DE BASE DE DATOS: BASEDOS
-- Tablas: clases y horarios
-- Autor: Manuel Rodríguez, Ricardo Hoyos
-- Fecha: 2025-10-16
-- =========================================================

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS basedos;
USE basedos;

-- =========================================================
-- TABLA: clases
-- =========================================================
CREATE TABLE clases (
  id_clase INT(11) NOT NULL AUTO_INCREMENT,
  titulo VARCHAR(100) NOT NULL,
  descripcion TEXT DEFAULT NULL,
  profesor_id INT(11) NOT NULL,
  precio DECIMAL(10,2) DEFAULT NULL,
  fecha_creacion DATETIME DEFAULT NULL,
  estado ENUM('Activa', 'Inactiva', 'Finalizada') DEFAULT 'Activa',
  PRIMARY KEY (id_clase)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Datos iniciales para la tabla 'clases'
INSERT INTO clases (id_clase, titulo, descripcion, profesor_id, precio, fecha_creacion, estado) VALUES
(1, 'Introducción a las redes neuronales', 'Aprenderás a dominar los tipos de aprendizaje que utilizan las redes neuronales.', 50, 1.00, '2025-10-14 00:00:00', 'Activa'),
(2, 'Introducción a la Programación en PHP', 'Curso básico sobre sintaxis, variables y estructuras de control en Python.', 30, 60.00, '2025-10-14 17:45:36', 'Activa'),
(4, 'Clase básica de ciberseguridad en aplicaciones web', 'Aplicaremos ataques a un sitio web vulnerable como DVWA.', 30, 1.00, '2025-10-15 21:03:12', 'Activa'),
(5, 'Curso de Roblox Studio', 'Aprenderemos a crear videojuegos de manera intuitiva y divertida.', 63, 80.00, '2025-10-15 21:35:38', 'Activa');

-- =========================================================
-- TABLA: horarios
-- =========================================================
CREATE TABLE horarios (
  id_horario INT(11) NOT NULL AUTO_INCREMENT,
  id_clase INT(11) NOT NULL,
  dia VARCHAR(20) NOT NULL,
  hora_inicio TIME DEFAULT NULL,
  hora_fin TIME DEFAULT NULL,
  PRIMARY KEY (id_horario),
  FOREIGN KEY (id_clase) REFERENCES clases(id_clase)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Datos iniciales para la tabla 'horarios'
INSERT INTO horarios (id_horario, id_clase, dia, hora_inicio, hora_fin) VALUES
(1, 1, 'Martes', NULL, NULL),
(2, 2, 'Jueves', NULL, NULL),
(4, 4, 'Jueves', NULL, NULL),
(5, 5, 'Miércoles', NULL, NULL);
