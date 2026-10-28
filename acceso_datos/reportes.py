import pymysql
from conexion.conexion_bd import obtener_conexion
from conexion.errores import traducir_error

def turnos_con_nombres():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT t.id_turno, CONCAT(pa.nombre, ' ', pa.apellido), CONCAT(pr.nombre, ' ', pr.apellido), DATE_FORMAT(t.fecha, '%d/%m/%Y'), TIME_FORMAT(t.hora, '%H:%i'), t.estado
            FROM turno t
            JOIN paciente pa ON t.dni_paciente = pa.dni
            JOIN profesional pr ON t.`matrícula_prof` = pr.`matrícula`
            ORDER BY t.fecha, t.hora;
        """)
        return cursor.fetchall()
    except pymysql.MySQLError as error:
        raise traducir_error(error) from error
    finally:
        conexion.close()

def turnos_por_especialidad():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT pr.especialidad, COUNT(*)
            FROM turno t JOIN profesional pr ON t.`matrícula_prof` = pr.`matrícula`
            GROUP BY pr.especialidad;
        """)
        return cursor.fetchall()
    except pymysql.MySQLError as error:
        raise traducir_error(error) from error
    finally:
        conexion.close()

def turnos_por_estado():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT estado, COUNT(*) FROM turno GROUP BY estado")
        return cursor.fetchall()
    except pymysql.MySQLError as error:
        raise traducir_error(error) from error
    finally:
        conexion.close()

def pacientes_sin_turnos():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT pa.dni, pa.nombre, pa.apellido
            FROM paciente pa LEFT JOIN turno t ON t.dni_paciente = pa.dni
            WHERE t.id_turno IS NULL;
        """)
        return cursor.fetchall()
    except pymysql.MySQLError as error:
        raise traducir_error(error) from error
    finally:
        conexion.close()
        