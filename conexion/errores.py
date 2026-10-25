import pymysql
 
 
class ErrorBaseDeDatos(Exception):
    """Error de base de datos con un mensaje listo para mostrar al usuario."""
 
 
_MENSAJES = {
    1044: "El usuario de la base de datos no tiene acceso a la base 'odontokinesis'.",
    1045: "Usuario o contraseña de MySQL incorrectos. Revisá el archivo conexion/config.ini.",
    1049: "La base de datos 'odontokinesis' no existe. Ejecutá el script tablas_mysql.sql.",
    1062: "Ya existe un registro con ese identificador.",
    1142: "El usuario de la base de datos no tiene permiso para realizar esta operación.",
    1146: "Falta una tabla en la base de datos. Ejecutá el script tablas_mysql.sql.",
    1406: "Uno de los datos ingresados es demasiado largo para su campo.",
    1451: "No se puede eliminar: hay turnos asociados a este registro.",
    1452: "El paciente o el profesional indicado no existe en la base de datos.",
    2003: "No se pudo conectar con el servidor MySQL. Verificá que esté iniciado.",
    3819: "Uno de los datos ingresados no cumple una restricción de la base de datos.",
}
 
 
def traducir_error(error):
    """Convierte un error de pymysql en un ErrorBaseDeDatos con mensaje claro."""
    codigo = error.args[0] if error.args and isinstance(error.args[0], int) else None
    mensaje = _MENSAJES.get(codigo, "Ocurrió un error inesperado en la base de datos.")
    return ErrorBaseDeDatos(mensaje)