# Consultas SQL documentadas - OdontoKinesis
Base de datos: MySQL, base `odontokinesis`, tablas `paciente`, `profesional` y `turno`.
Las consultas se ejecutan desde Python con `pymysql`; los valores variables se envían como parámetros (`%s`), nunca concatenados en el texto de la sentencia.
Los resultados de ejemplo corresponden a los datos de prueba originales de `tablas_mysql.sql`.
> Las columnas con tilde (`matrícula`, `matrícula_prof`) van entre comillas invertidas.
---
## A. Consultas de la pantalla Consultas (`acceso_datos/modelo_datos.py`)
### A.1 Turnos por fecha
Lista los turnos de un día. En la aplicación la fecha se ingresa como dd/mm/aaaa y se convierte al tipo `DATE`.
```sql
SELECT id_turno, dni_paciente, `matrícula_prof`, fecha, hora, estado
FROM turno
WHERE fecha = '2026-06-12';
### A.2 Turnos por profesional
Lista los turnos asignados a un profesional, buscado por su matrícula.
```sql
SELECT id_turno, dni_paciente, `matrícula_prof`, fecha, hora, estado
FROM turno
WHERE `matrícula_prof` = 'MP1234';
### A.3 Turnos por paciente
Lista los turnos de un paciente, buscado por su DNI.
```sql
SELECT id_turno, dni_paciente, `matrícula_prof`, fecha, hora, estado
FROM turno
WHERE dni_paciente = '12345678';
Resultado de ejemplo (1 fila):
| id_turno | dni_paciente | matrícula_prof | fecha | hora | estado |
|---|---|---|---|---|---|
| 1 | 12345678 | MP1234 | 2026-06-10 | 10:30:00 | Confirmado |
### A.4 Turnos por estado
Lista los turnos que están en un estado (Reservado, Confirmado, Atendido o Cancelado), sin distinguir mayúsculas.
```sql
SELECT id_turno, dni_paciente, `matrícula_prof`, fecha, hora, estado
FROM turno
WHERE LOWER(estado) = LOWER('Confirmado');
Resultado de ejemplo (4 filas):
| id_turno | dni_paciente | matrícula_prof | fecha | hora | estado |
|---|---|---|---|---|---|
| 1 | 12345678 | MP1234 | 2026-06-10 | 10:30:00 | Confirmado |
| 3 | 11223344 | MP9012 | 2026-06-12 | 09:00:00 | Confirmado |
| 7 | 55667788 | MP5678 | 2026-06-15 | 10:00:00 | Confirmado |
| 10 | 88990011 | MP7890 | 2026-06-18 | 09:30:00 | Confirmado |
### A.5 Cantidad de turnos por profesional
Cuenta cuántos turnos tiene cada profesional (consulta con agrupación).
```sql
SELECT `matrícula_prof`, COUNT(*)
FROM turno
GROUP BY `matrícula_prof`;
## B. Reportes (`acceso_datos/reportes.py`)
### B.1 Turnos con pacientes y profesionales
Une las tres tablas (`JOIN`) para mostrar cada turno con el nombre del paciente y del profesional, en lugar de sus códigos. La fecha y la hora se formatean como en el resto de la aplicación.
```sql
SELECT t.id_turno,
       CONCAT(pa.nombre, ' ', pa.apellido),
       CONCAT(pr.nombre, ' ', pr.apellido),
       DATE_FORMAT(t.fecha, '%d/%m/%Y'),
       TIME_FORMAT(t.hora, '%H:%i'),
       t.estado
FROM turno t
JOIN paciente pa ON t.dni_paciente = pa.dni
JOIN profesional pr ON t.`matrícula_prof` = pr.`matrícula`
ORDER BY t.fecha, t.hora;