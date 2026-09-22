import tkinter as tk
from login_view import LoginVentana
 
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    aplicacion = LoginVentana(ventana_principal)
    ventana_principal.mainloop()
 