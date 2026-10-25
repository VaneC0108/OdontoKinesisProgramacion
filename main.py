 
import traceback
import tkinter as tk
from tkinter import messagebox
 
from interfaz.menu_view import MenuPrincipal
 
 
def _error_inesperado(tipo, valor, traza):
    """Red de seguridad: cualquier error no previsto se informa en una ventana
    (y además se imprime completo en la terminal para poder depurarlo)."""
    traceback.print_exception(tipo, valor, traza)
    messagebox.showerror(
        "Error inesperado",
        "Ocurrió un error inesperado en la aplicación.\n\nDetalle: " + str(valor),
    )
 
 
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    ventana_principal.report_callback_exception = _error_inesperado
    aplicacion = MenuPrincipal(ventana_principal, usuario="Invitado")
    ventana_principal.mainloop()
 