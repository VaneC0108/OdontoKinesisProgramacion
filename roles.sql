-- roles.sql: roles de acceso de la base odontokinesis (MySQL)
-- Se ejecuta con el usuario root. Las contraseñas son de ejemplo.
-- Se puede volver a ejecutar sin errores (borra los usuarios antes de crearlos).

DROP USER IF EXISTS 'admin_odonto'@'localhost';
DROP USER IF EXISTS 'recepcion_odonto'@'localhost';
DROP USER IF EXISTS 'profesional_odonto'@'localhost';
DROP USER IF EXISTS 'app_odonto'@'localhost';

-- Administración: todos los permisos, solo sobre la base odontokinesis.
CREATE USER 'admin_odonto'@'localhost' IDENTIFIED BY 'ClaveAdmin123';
GRANT ALL PRIVILEGES ON odontokinesis.* TO 'admin_odonto'@'localhost';

-- Recepción: consulta, carga y modifica datos; solo puede borrar turnos.
CREATE USER 'recepcion_odonto'@'localhost' IDENTIFIED BY 'ClaveRecep123';
GRANT SELECT, INSERT, UPDATE ON odontokinesis.* TO 'recepcion_odonto'@'localhost';
GRANT DELETE ON odontokinesis.turno TO 'recepcion_odonto'@'localhost';

-- Profesional: solo consulta y puede cambiar el estado de un turno.
CREATE USER 'profesional_odonto'@'localhost' IDENTIFIED BY 'ClaveProf123';
GRANT SELECT ON odontokinesis.* TO 'profesional_odonto'@'localhost';
GRANT UPDATE (estado) ON odontokinesis.turno TO 'profesional_odonto'@'localhost';

-- Aplicación (usuario con el que se conecta main.py): alta, consulta,
-- modificación y baja sobre la base, sin permisos para crear ni borrar
-- tablas, ni para dar permisos a otros usuarios. Reemplaza al uso de root.
CREATE USER 'app_odonto'@'localhost' IDENTIFIED BY 'ClaveApp123';
GRANT SELECT, INSERT, UPDATE, DELETE ON odontokinesis.* TO 'app_odonto'@'localhost';
