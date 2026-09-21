-- Creación de la tabla Paciente 
CREATE TABLE paciente (
    dni VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Creación de la tabla Profesional 
CREATE TABLE profesional (
    matrícula VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    especialidad VARCHAR(20) NOT NULL,
    teléfono VARCHAR(20) NOT NULL
);

-- Creación de la tabla Turnos 
CREATE TABLE turno (
    id_turno SERIAL PRIMARY KEY,
    dni_paciente VARCHAR(10) NOT NULL,
    matrícula_prof VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(20) CHECK (estado IN ('Reservado', 'Confirmado', 'Atendido', 'Cancelado')) NOT NULL,
    CONSTRAINT fk_paciente FOREIGN KEY (dni_paciente) REFERENCES paciente(dni),
    CONSTRAINT fk_profesional FOREIGN KEY (matrícula_prof) REFERENCES profesional(matrícula)
);

-- Inserción de 10 datos de prueba para Pacientes
INSERT INTO paciente (dni, nombre, apellido, telefono, email) VALUES 
('12345678', 'Juan', 'Pérez', '3511234567', 'juan.perez@email.com'),
('87654321', 'María', 'Gómez', '3519876543', 'maria.gomez@email.com'),
('11223344', 'Carlos', 'Rodríguez', '3514567890', 'carlos.rodriguez@email.com'),
('22334455', 'Ana', 'Martínez', '3517890123', 'ana.martinez@email.com'),
('33445566', 'Lucas', 'Fernández', '3513216549', 'lucas.fernandez@email.com'),
('44556677', 'Sofía', 'López', '3516549870', 'sofia.lopez@email.com'),
('55667788', 'Mateo', 'García', '3519873210', 'mateo.garcia@email.com'),
('66778899', 'Valentina', 'Sánchez', '3511472583', 'valentina.sanchez@email.com'),
('77889900', 'Diego', 'Ramírez', '3512583691', 'diego.ramirez@email.com'),
('88990011', 'Lucía', 'Torres', '3513692584', 'lucia.torres@email.com');

-- Inserción de Profesionales de prueba
INSERT INTO profesional (matrícula, nombre, apellido, especialidad, teléfono) VALUES 
('MP1234', 'Carlos', 'López', 'Odontología', '3511111111'),
('MP5678', 'Ana', 'Torres', 'Odontología', '3512222222'),
('MP9012', 'Esteban', 'Giménez', 'Kinesiología', '3513333333'),
('MP3456', 'Mariana', 'Ruiz', 'Kinesiología', '3514444444'),
('MP7890', 'Javier', 'Benítez', 'Odontología', '3515555555');

-- Inserción de 10 datos de prueba para Turnos
INSERT INTO turno (dni_paciente, matrícula_prof, fecha, hora, estado) VALUES 
('12345678', 'MP1234', '2026-06-10', '10:30:00', 'Confirmado'),
('87654321', 'MP5678', '2026-06-11', '15:00:00', 'Reservado'),
('11223344', 'MP9012', '2026-06-12', '09:00:00', 'Confirmado'),
('22334455', 'MP3456', '2026-06-12', '11:30:00', 'Cancelado'),
('33445566', 'MP7890', '2026-06-13', '14:00:00', 'Atendido'),
('44556677', 'MP1234', '2026-06-14', '16:15:00', 'Reservado'),
('55667788', 'MP5678', '2026-06-15', '10:00:00', 'Confirmado'),
('66778899', 'MP9012', '2026-06-16', '11:00:00', 'Reservado'),
('77889900', 'MP3456', '2026-06-17', '15:30:00', 'Atendido'),
('88990011', 'MP7890', '2026-06-18', '09:30:00', 'Confirmado');

