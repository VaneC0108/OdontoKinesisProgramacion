import functools
from tkinter import messagebox
from conexion.errores import ErrorBaseDeDatos

def mostrar_errores_bd(metodo):
    @functools.wraps(metodo)
    def envoltura(*args, **kwargs):
        try:
            return metodo(*args, **kwargs)
        except ErrorBaseDeDatos as error:
            messagebox.showwarning("Atención", str(error))
        except Exception as error:
            # Si el error contiene código 1217 o 1451 de clave foránea
            texto = str(error)
            if "1217" in texto or "1451" in texto:
                messagebox.showwarning(
                    "Atención",
                    "No se puede eliminar: hay turnos asociados a este registro."
                )
            else:
                messagebox.showerror(
                    "Error inesperado",
                    f"Ocurrió un error en la aplicación.\n\nDetalle: {error}"
                )
    return envoltura