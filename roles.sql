USE odontokinesis; 
CREATE USER 'admin_odonto'@'localhost' IDENTIFIED BY 'ClaveAdmin123';
GRANT ALL PRIVILEGES ON odontokinesis.* TO 'admin_odonto'@'localhost';

CREATE USER 'recepcion_odonto'@'localhost' IDENTIFIED BY 'ClaveRecep123';
GRANT SELECT, INSERT, UPDATE ON odontokinesis.* TO 'recepcion_odonto'@'localhost';
GRANT DELETE ON odontokinesis.turno TO 'recepcion_odonto'@'localhost';

CREATE USER 'profesional_odonto'@'localhost' IDENTIFIED BY 'ClaveProf123';
GRANT SELECT ON odontokinesis.* TO 'profesional_odonto'@'localhost';
GRANT UPDATE (estado) ON odontokinesis.turno TO 'profesional_odonto'@'localhost';
