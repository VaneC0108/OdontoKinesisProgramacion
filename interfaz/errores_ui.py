import functools
from tkinter import messagebox
 
from conexion.errores import ErrorBaseDeDatos
 
 
def mostrar_errores_bd(metodo):
    @functools.wraps(metodo)
    def envoltura(*args, **kwargs):
        try:
            return metodo(*args, **kwargs)
        except ErrorBaseDeDatos as error:
            messagebox.showerror("Error de base de datos", str(error))
    return envoltura