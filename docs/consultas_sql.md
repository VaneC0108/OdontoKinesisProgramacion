# Documentación de Consultas SQL - Módulo de Reportes (OdontoKinesis)

Este documento detalla las consultas SQL utilizadas en el módulo de reportes avanzados para la extracción de información del sistema.

## 1. Turnos con Pacientes y Profesionales
Permite listar el detalle completo de los turnos programados, vinculando los datos de los pacientes y los profesionales asignados mediante uniones (`JOIN`).

```sql
SELECT 
    t.id_turno, 
    t.fecha, 
    t.hora, 
    t.estado, 
    p.nombre AS paciente_nombre, 
    p.apellido AS paciente_apellido, 
    pr.nombre AS profesional_nombre, 
    pr.apellido AS profesional_apellido, 
    pr.especialidad 
FROM turnos t
JOIN pacientes p ON t.id_paciente = p.id_paciente
JOIN profesionales pr ON t.id_profesional = pr.id_profesional;
SELECT 
    pr.especialidad, 
    COUNT(t.id_turno) AS total_turnos
FROM turnos t
JOIN profesionales pr ON t.id_profesional = pr.id_profesional
GROUP BY pr.especialidad;
SELECT 
    estado, 
    COUNT(*) AS cantidad 
FROM turnos 
GROUP BY estado;
SELECT 
    p.id_paciente, 
    p.nombre, 
    p.apellido, 
    p.telefono, 
    p.correo 
FROM pacientes p
LEFT JOIN turnos t ON p.id_paciente = t.id_paciente
WHERE t.id_turno IS NULL;