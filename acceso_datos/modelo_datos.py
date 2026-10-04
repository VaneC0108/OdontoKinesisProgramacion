from conexion.conexion_bd import obtener_conexion
 

 
def obtener_pacientes():
    """Devuelve todos los pacientes de la base, como lista de diccionarios."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT dni, nombre, apellido, telefono, email "
            "FROM paciente ORDER BY dni"
        )
        filas = cursor.fetchall()
        return [
            {"dni": f[0], "nombre": f[1], "apellido": f[2], "telefono": f[3], "email": f[4]}
            for f in filas
        ]
    finally:
        conexion.close()
 
 
def obtener_paciente_por_dni(dni):
    """Devuelve un paciente (diccionario) o None si no existe en la base."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT dni, nombre, apellido, telefono, email "
            "FROM paciente WHERE dni = %s",
            (dni,),
        )
        fila = cursor.fetchone()
        if fila is None:
            return None
        return {"dni": fila[0], "nombre": fila[1], "apellido": fila[2],
                "telefono": fila[3], "email": fila[4]}
    finally:
        conexion.close()
 
 
def crear_paciente(paciente):
    """Inserta un paciente nuevo en la base."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO paciente (dni, nombre, apellido, telefono, email) "
            "VALUES (%s, %s, %s, %s, %s)",
            (paciente["dni"], paciente["nombre"], paciente["apellido"],
             paciente["telefono"], paciente["email"]),
        )
        conexion.commit()
    finally:
        conexion.close()
 
 
def actualizar_paciente(dni, paciente):
    """Actualiza los datos de un paciente existente (lo busca por dni)."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE paciente SET nombre=%s, apellido=%s, telefono=%s, email=%s "
            "WHERE dni=%s",
            (paciente["nombre"], paciente["apellido"], paciente["telefono"],
             paciente["email"], dni),
        )
        conexion.commit()
    finally:
        conexion.close()
 
 
def eliminar_paciente(dni):
    """Elimina un paciente de la base, por dni."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM paciente WHERE dni=%s", (dni,))
        conexion.commit()
    finally:
        conexion.close()

 
def obtener_profesionales():
    """Devuelve todos los profesionales de la base, como lista de diccionarios."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'SELECT `matrícula`, nombre, apellido, especialidad, `teléfono` '
            'FROM profesional ORDER BY `matrícula`'
        )
        filas = cursor.fetchall()
        return [
            {"matricula": f[0], "nombre": f[1], "apellido": f[2],
             "especialidad": f[3], "telefono": f[4]}
            for f in filas
        ]
    finally:
        conexion.close()
 
 
def obtener_profesional_por_matricula(matricula):
    """Devuelve un profesional (diccionario) o None si no existe."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'SELECT `matrícula`, nombre, apellido, especialidad, `teléfono` '
            'FROM profesional WHERE `matrícula` = %s',
            (matricula,),
        )
        fila = cursor.fetchone()
        if fila is None:
            return None
        return {"matricula": fila[0], "nombre": fila[1], "apellido": fila[2],
                "especialidad": fila[3], "telefono": fila[4]}
    finally:
        conexion.close()
 
 
def crear_profesional(profesional):
    """Inserta un profesional nuevo en la base."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'INSERT INTO profesional (`matrícula`, nombre, apellido, especialidad, `teléfono`) '
            "VALUES (%s, %s, %s, %s, %s)",
            (profesional["matricula"], profesional["nombre"], profesional["apellido"],
             profesional["especialidad"], profesional["telefono"]),
        )
        conexion.commit()
    finally:
        conexion.close()
 
 
def actualizar_profesional(matricula, profesional):
    """Actualiza los datos de un profesional existente (lo busca por matrícula)."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'UPDATE profesional SET nombre=%s, apellido=%s, especialidad=%s, `teléfono`=%s '
            'WHERE `matrícula`=%s',
            (profesional["nombre"], profesional["apellido"], profesional["especialidad"],
             profesional["telefono"], matricula),
        )
        conexion.commit()
    finally:
        conexion.close()
 
 
def eliminar_profesional(matricula):
    """Elimina un profesional de la base, por matrícula."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM profesional WHERE `matrícula`=%s', (matricula,))
        conexion.commit()
    finally:
        conexion.close()
 
 
from datetime import datetime as _datetime, timedelta as _timedelta
 
 
def _texto_a_fecha(texto_ddmmaaaa):
    return _datetime.strptime(texto_ddmmaaaa, "%d/%m/%Y").date()
 
 
def _fecha_a_texto(fecha):
    return fecha.strftime("%d/%m/%Y")
 
 
def _texto_a_hora(texto_hhmm):
    return _datetime.strptime(texto_hhmm, "%H:%M").time()
 
 
def _hora_a_texto(hora):
    if isinstance(hora, _timedelta):
        total_segundos = int(hora.total_seconds())
        horas, resto = divmod(total_segundos, 3600)
        minutos, _segundos = divmod(resto, 60)
        return f"{horas:02d}:{minutos:02d}"
    return hora.strftime("%H:%M")
 
 
def obtener_turnos():
    """Devuelve todos los turnos de la base, como lista de diccionarios."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'SELECT id_turno, dni_paciente, `matrícula_prof`, fecha, hora, estado '
            'FROM turno ORDER BY id_turno'
        )
        filas = cursor.fetchall()
        return [
            {"id_turno": f[0], "dni_paciente": f[1], "matricula_prof": f[2],
             "fecha": _fecha_a_texto(f[3]), "hora": _hora_a_texto(f[4]), "estado": f[5]}
            for f in filas
        ]
    finally:
        conexion.close()
 
 
def obtener_turnos_por_paciente(dni):
    """Devuelve los turnos de un paciente puntual."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'SELECT id_turno, dni_paciente, `matrícula_prof`, fecha, hora, estado '
            'FROM turno WHERE dni_paciente = %s ORDER BY id_turno',
            (dni,),
        )
        filas = cursor.fetchall()
        return [
            {"id_turno": f[0], "dni_paciente": f[1], "matricula_prof": f[2],
             "fecha": _fecha_a_texto(f[3]), "hora": _hora_a_texto(f[4]), "estado": f[5]}
            for f in filas
        ]
    finally:
        conexion.close()
 
 
def existe_choque_turno(matricula_prof, fecha_texto, hora_texto, ignorar_id=None):
    """True si ese profesional ya tiene un turno en esa fecha y hora exactas."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        fecha = _texto_a_fecha(fecha_texto)
        hora = _texto_a_hora(hora_texto)
        if ignorar_id is None:
            cursor.execute(
                'SELECT COUNT(*) FROM turno '
                'WHERE `matrícula_prof`=%s AND fecha=%s AND hora=%s',
                (matricula_prof, fecha, hora),
            )
        else:
            cursor.execute(
                'SELECT COUNT(*) FROM turno '
                'WHERE `matrícula_prof`=%s AND fecha=%s AND hora=%s AND id_turno != %s',
                (matricula_prof, fecha, hora, ignorar_id),
            )
        return cursor.fetchone()[0] > 0
    finally:
        conexion.close()
 
 
def crear_turno(turno):
    """Inserta un turno nuevo en la base y devuelve el id_turno asignado.
 
    No mandamos id_turno en el INSERT: en MySQL esa columna es
    AUTO_INCREMENT, así que la base lo asigna sola. cursor.lastrowid
    nos devuelve el id que acaba de generar.
    """
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'INSERT INTO turno (dni_paciente, `matrícula_prof`, fecha, hora, estado) '
            "VALUES (%s, %s, %s, %s, %s)",
            (turno["dni_paciente"], turno["matricula_prof"],
             _texto_a_fecha(turno["fecha"]), _texto_a_hora(turno["hora"]), turno["estado"]),
        )
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()
 
 
def actualizar_turno(id_turno, turno):
    """Actualiza un turno existente (lo busca por id_turno)."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'UPDATE turno SET dni_paciente=%s, `matrícula_prof`=%s, fecha=%s, hora=%s, estado=%s '
            "WHERE id_turno=%s",
            (turno["dni_paciente"], turno["matricula_prof"],
             _texto_a_fecha(turno["fecha"]), _texto_a_hora(turno["hora"]),
             turno["estado"], id_turno),
        )
        conexion.commit()
    finally:
        conexion.close()
 
 
def eliminar_turno(id_turno):
    """Elimina un turno de la base, por id_turno."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM turno WHERE id_turno=%s", (id_turno,))
        conexion.commit()
    finally:
        conexion.close()
 
 
def _filas_a_turnos(filas):
    return [
        {"id_turno": f[0], "dni_paciente": f[1], "matricula_prof": f[2],
         "fecha": _fecha_a_texto(f[3]), "hora": _hora_a_texto(f[4]), "estado": f[5]}
        for f in filas
    ]
 
 
def obtener_turnos_por_fecha(fecha_texto):
    """Turnos en una fecha puntual (texto dd/mm/aaaa)."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'SELECT id_turno, dni_paciente, `matrícula_prof`, fecha, hora, estado '
            'FROM turno WHERE fecha = %s ORDER BY id_turno',
            (_texto_a_fecha(fecha_texto),),
        )
        return _filas_a_turnos(cursor.fetchall())
    finally:
        conexion.close()
 
 
def obtener_turnos_por_profesional(matricula):
    """Turnos de un profesional puntual."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'SELECT id_turno, dni_paciente, `matrícula_prof`, fecha, hora, estado '
            'FROM turno WHERE `matrícula_prof` = %s ORDER BY id_turno',
            (matricula,),
        )
        return _filas_a_turnos(cursor.fetchall())
    finally:
        conexion.close()
 
 
def obtener_turnos_por_estado(estado):
    """Turnos que están en un estado puntual (sin importar mayúsc/minúsc)."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'SELECT id_turno, dni_paciente, `matrícula_prof`, fecha, hora, estado '
            'FROM turno WHERE LOWER(estado) = LOWER(%s) ORDER BY id_turno',
            (estado,),
        )
        return _filas_a_turnos(cursor.fetchall())
    finally:
        conexion.close()
 
 
def obtener_cantidad_turnos_por_profesional():
    """Devuelve {matricula: cantidad_de_turnos} para los profesionales que tienen turnos."""
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            'SELECT `matrícula_prof`, COUNT(*) FROM turno GROUP BY `matrícula_prof`'
        )
        return {fila[0]: fila[1] for fila in cursor.fetchall()}
    finally:
        conexion.close()
 
 
ESTADOS_TURNO = ["Reservado", "Confirmado", "Atendido", "Cancelado"]
ESPECIALIDADES = ["Odontología", "Kinesiología"]
 