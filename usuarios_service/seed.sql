-- =========================================================
-- SCRIPT DE BASE DE DATOS: PLATAFORMA EDUCATIVA
-- Tablas: roles y usuarios
-- Autor: Manuel Rodríguez, Ricardo hoyos
-- Fecha: 2025-10-16
-- =========================================================

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS plataformaeducativa;
USE plataformaeducativa;

-- =========================================================
-- TABLA: roles
-- =========================================================
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Datos iniciales para roles
INSERT INTO roles (id, nombre) VALUES
(1, 'Admin'),
(2, 'Cliente'),
(3, 'Docente');

-- =========================================================
-- TABLA: usuarios
-- =========================================================
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Usuario VARCHAR(255) NOT NULL,
    Clave VARCHAR(255) NOT NULL,
    Nombre_Completo VARCHAR(255) NOT NULL,
    Telefono VARCHAR(15) NOT NULL,
    Direccion VARCHAR(255) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    rol_id INT NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    experiencia_laboral VARCHAR(255) DEFAULT NULL,
    hoja_vida_path VARCHAR(255) DEFAULT NULL,
    titulo_profesional VARCHAR(100) DEFAULT NULL,
    estado_verificacion ENUM('Pendiente','Verificado','Rechazado') DEFAULT 'Pendiente',
    CONSTRAINT fk_usuarios_roles FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- =========================================================
-- DATOS DE EJEMPLO PARA USUARIOS
-- =========================================================
INSERT INTO usuarios (id, Usuario, Clave, Nombre_Completo, Telefono, Direccion, Email, rol_id, activo, experiencia_laboral, hoja_vida_path, titulo_profesional, estado_verificacion) VALUES
(30, 'Ricardo002', '$2y$10$3KyQS3RjtTE2WTTWq8U17ONeyqGMQVjUjzgH3OJI7CTMonJvRpWy.', 'Ricardo Hoyos', '234141', 'calle 35', 'Ricardo0@gmail.com', 3, 1, NULL, NULL, NULL, 'Pendiente'),
(48, 'cliente004', '$2y$10$bxJSwtZGGQi.JbQ9xthM8.k1OLttH9JpfhGg51jwXckxHgW5Ny0Xu', 'Carlos', '3104567890', 'Calle 45 #12-34', 'carlos.@example.com', 3, 1, NULL, NULL, NULL, 'Pendiente'),
(50, 'Hugo88', '$2y$10$uVXXZ.gxP4nECWEbSULbYuHM98kqF.Y1wk1IkUE9hoceTKjMNxqri', 'Hugo Orlando Rodriguez', '3218889910', 'carre 9', 'Hugo88@gmail.com', 3, 1, '0', '682e2558201ab_Auditoria_Criptografica_y_Web.pdf', 'Ingeniero de software', 'Pendiente'),
(51, 'cliente004', '$2y$10$LzVdYEQ1M6Uht3NthyIsUuVS16em08dBBxiIW.sQu2anGUs46B3ku', 'Juan Pérez Actualizado', '3205559999', 'Calle 15 #10-45', 'juan.actualizado@correo.com', 3, 1, '0', '682e29bbf10b9_ref 1 bosques pop.pdf', 'Lenguas modernas', 'Verificado'),
(52, 'cliente004', '$2y$10$kT4mAS8Z10kNkyfpJmXu3u8U3QdxrXY1RUoByMgDtGUPCHf0ZuECq', 'Carlos', '3104567890', 'Calle 45 #12-34', 'carlos.@example.com', 3, 1, 'Abogado penalista', '682e3312d35b2_cv Juan 1.pdf', 'Abogado', 'Pendiente'),
(53, 'asld23', '$2y$10$kxEqlsdA7VzVCQO2KR/HUOpR5hrhF3OVOZJMdC5y/smh5eySu9qz6', 'asld', '123', 'asld23@gmail.com', 'asld23@gmail.com', 2, 1, NULL, NULL, NULL, 'Pendiente'),
(56, 'cliente004', '$2y$10$Ala2ucMHAhCo7tmudjoRN.B4P56o/jZ82xUdsqvNgsxbntp30tCam', 'Carlos', '3104567890', 'Calle 45 #12-34', 'carlos.@example.com', 3, 1, NULL, NULL, NULL, 'Pendiente'),
(61, 'manuel123', '$2b$12$n0070fmfct9NY1iaZMaxG.ElRZ3RBDJPoaP49ejcfm3d9yLa0i8VO', 'Manuel Rodríguez', '3001112233', 'Calle 45', 'manuel@example.com', 2, 1, NULL, NULL, NULL, 'Pendiente'),
(62, 'Juanjose002', '$2b$12$6zIGg2c.1Cr9WqNBGCKcd.YI2O3EItwAso737wPUYjKTe8bKs7kOS', 'Juan Jose Meza', '300111444', 'Calle 46', 'Juanjose123@example.com', 2, 1, NULL, NULL, NULL, 'Pendiente'),
(63, 'DanielFC123', '$2b$12$JsyDCT0jseU5skcxeojmNuV5f7DVAiAazEPZ6DwjGovvFEKOKpITu', 'Daniel Fernando cobo', '3333333', 'Casa 2', 'DFC123@example.com', 3, 1, NULL, NULL, NULL, 'Pendiente');
-- AUTO_INCREMENT
-- =========================================================
ALTER TABLE roles AUTO_INCREMENT = 4;
ALTER TABLE usuarios AUTO_INCREMENT = 64;

COMMIT;
