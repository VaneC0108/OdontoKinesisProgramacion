import pymysql

HOST = "localhost"
PUERTO = 3306
BASE_DE_DATOS = "odontokinesis"
USUARIO = "root"
CONTRASENA = "TU_CONTRASEÑA_ACA"
 
 
def obtener_conexion():
    """Abre y devuelve una conexión nueva a la base odontokinesis."""
    return pymysql.connect(
        host=HOST,
        port=PUERTO,
        database=BASE_DE_DATOS,
        user=USUARIO,
        password=CONTRASENA,
        charset="utf8mb4",
    )