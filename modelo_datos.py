pacientes = [
    {"dni": "30111222", "nombre": "Marta", "apellido": "Perez",
     "telefono": "3511234567", "email": "marta.perez@mail.com"},
    {"dni": "28999888", "nombre": "Carlos", "apellido": "Diaz",
     "telefono": "3517654321", "email": "carlos.diaz@mail.com"},
]
 
profesionales = [
    {"matricula": "K-1024", "nombre": "Eliana Roxana", "apellido": "Canovas",
     "especialidad": "Kinesiología", "telefono": "3512223344"},
    {"matricula": "O-2048", "nombre": "Mariana Rosa", "apellido": "Canovas",
     "especialidad": "Odontología", "telefono": "3515556677"},
]
 
turnos = [
    {"id_turno": 1, "dni_paciente": "30111222", "matricula_prof": "O-2048",
     "fecha": "2026-09-25", "hora": "10:00", "estado": "Reservado"},
]
 
_ultimo_id_turno = 1
 
 
def proximo_id_turno():
    """Devuelve un id incremental simple para nuevos turnos (mock de SERIAL)."""
    global _ultimo_id_turno
    _ultimo_id_turno += 1
    return _ultimo_id_turno
 
 
ESTADOS_TURNO = ["Reservado", "Confirmado", "Atendido", "Cancelado"]
ESPECIALIDADES = ["Odontología", "Kinesiología"]