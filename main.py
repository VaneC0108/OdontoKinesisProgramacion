import tkinter as tk
from interfaz.menu_view import MenuPrincipal
 
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    aplicacion = MenuPrincipal(ventana_principal, usuario="Invitado")
    ventana_principal.mainloop()
 