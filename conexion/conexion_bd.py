import configparser
import os
 
import pymysql
 
from conexion.errores import ErrorBaseDeDatos, traducir_error
 
_RUTA_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
 
 
def _leer_configuracion():
    if not os.path.exists(_RUTA_CONFIG):
        raise ErrorBaseDeDatos(
            "Falta el archivo conexion/config.ini. Copiá conexion/config.example.ini "
            "como config.ini y completá tu usuario y contraseña de MySQL."
        )
    config = configparser.ConfigParser()
    config.read(_RUTA_CONFIG, encoding="utf-8")
    if "mysql" not in config:
        raise ErrorBaseDeDatos("El archivo conexion/config.ini no tiene la sección [mysql].")
    return config["mysql"]
 
 
def obtener_conexion():
    """Abre y devuelve una conexión nueva a la base odontokinesis."""
    datos = _leer_configuracion()
    try:
        return pymysql.connect(
            host=datos.get("host", "localhost"),
            port=datos.getint("puerto", 3306),
            database=datos.get("base_de_datos", "odontokinesis"),
            user=datos.get("usuario", ""),
            password=datos.get("contrasena", ""),
            charset="utf8mb4",
        )
    except pymysql.MySQLError as error:
        raise traducir_error(error) from error
 