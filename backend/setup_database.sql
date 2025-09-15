-- Script para crear la base de datos y usuario para el sistema de golf
-- Ejecutar como usuario administrador de PostgreSQL

-- Crear base de datos
CREATE DATABASE golf_tournament;

-- Crear usuario (opcional, puedes usar postgres directamente)
-- CREATE USER golf_user WITH ENCRYPTED PASSWORD 'your_password_here';

-- Dar permisos al usuario
-- GRANT ALL PRIVILEGES ON DATABASE golf_tournament TO golf_user;

-- Conectar a la base de datos
\c golf_tournament;

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Verificar que todo esté listo
SELECT 'Database golf_tournament created successfully!' as status;