# Documentación de Consultas SQL - OdontoKinesis

Este archivo contiene el detalle de las consultas SQL utilizadas en las distintas pantallas del sistema.

## 1. Pantalla de Consultas (Consultas Simples)

### A. Turnos por Fecha
* **Qué hace:** Filtra los turnos programados para una fecha específica.
* **Sentencia SQL:** `SELECT * FROM turno WHERE fecha = '2026-06-12';`

### B. Turnos por Matrícula del Profesional
* **Qué hace:** Muestra todos los turnos asignados a un profesional en particular.
* **Sentencia SQL:** `SELECT * FROM turno WHERE matrícula_prof = 'MP1234';`

### C. Turnos por DNI del Paciente
* **Qué hace:** Busca el historial o los turnos de un paciente específico por su DNI.
* **Sentencia SQL:** `SELECT * FROM turno WHERE dni_paciente = '12345678';`

### D. Turnos por Estado
* **Qué hace:** Filtra los turnos según su estado actual (por ejemplo, Confirmados).
* **Sentencia SQL:** `SELECT * FROM turno WHERE estado = 'Confirmado';`

### E. Conteo de Turnos por Profesional
* **Qué hace:** Agrupa los turnos por matrícula para saber cuántos tiene asignados cada profesional.
* **Sentencia SQL:** `SELECT matrícula_prof, COUNT(*) FROM turno GROUP BY matrícula_prof;`
## 2. Módulo de Reportes

### A. Turnos con Pacientes y Profesionales
* **Qué hace:** Trae el detalle de los turnos uniendo los datos del paciente y del profesional.
* **Sentencia SQL:** 
`SELECT t.id_turno, t.fecha, t.hora, t.estado, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido, pr.nombre AS profesional_nombre, pr.apellido AS profesional_apellido, pr.especialidad FROM turno t JOIN paciente p ON t.dni_paciente = p.dni JOIN profesional pr ON t.matrícula_prof = pr.matrícula;`

### B. Reporte por Rango de Fechas
* **Qué hace:** Filtra los turnos comprendidos entre dos fechas determinadas.
* **Sentencia SQL:** `SELECT * FROM turno WHERE fecha BETWEEN '2026-06-01' AND '2026-06-30';`

### C. Turnos por Especialidad
* **Qué hace:** Permite filtrar los turnos según la especialidad médica del profesional.
* **Sentencia SQL:** `SELECT t.* FROM turno t JOIN profesional pr ON t.matrícula_prof = pr.matrícula WHERE pr.especialidad = 'Kinesiología';`

### D. Resumen de Turnos por Estado
* **Qué hace:** Cuenta cuántos turnos hay agrupados por cada estado.
* **Sentencia SQL:** `SELECT estado, COUNT(*) AS total_turnos FROM turno GROUP BY estado;`