import tkinter as tk
from tkinter import messagebox

ventana = tk.Tk()

class LoginVentana:
    def __init__(self, ventana_raiz):
        # 'ventana_raiz' es la ventana principal del sistema
        self.ventana_raiz = ventana_raiz
        self.ventana_raiz.title("OdontoKinesis - Control de Acceso")
        self.ventana_raiz.geometry("420x340")
        self.ventana_raiz.resizable(False, False)
        
        marco_central = tk.Frame(self.ventana_raiz)
        marco_central.pack(padx=20, pady=20, expand=True)
        
        etiqueta_titulo = tk.Label(marco_central, text="ODONTOKINESIS", font=("Arial", 16, "bold"))
        etiqueta_titulo.pack(pady=(0, 5))
        
        etiqueta_subtitulo = tk.Label(marco_central, text="Iniciar Sesión", font=("Arial", 11))
        etiqueta_subtitulo.pack(pady=(0, 20))
       
        etiqueta_usuario = tk.Label(marco_central, text="Usuario / DNI:", font=("Arial", 10))
        etiqueta_usuario.pack(anchor="w")
        
        self.campo_usuario = tk.Entry(marco_central, width=32, font=("Arial", 10))
        self.campo_usuario.pack(pady=(2, 10))
        
        etiqueta_clave = tk.Label(marco_central, text="Contraseña:", font=("Arial", 10))
        etiqueta_clave.pack(anchor="w")
        
        self.campo_clave = tk.Entry(marco_central, width=32, show="•", font=("Arial", 10))
        self.campo_clave.pack(pady=(2, 20))
        
        # Botón de acción para ingresar
        boton_ingresar = tk.Button(
            marco_central, 
            text="Iniciar Sesión", 
            font=("Arial", 10, "bold"),
            bg="#0288D1", 
            fg="white", 
            padx=10, 
            pady=4,
            command=self.validar_acceso
        )
        boton_ingresar.pack(fill="x")
        
    def validar_acceso(self):
        usuario_ingresado = self.campo_usuario.get().strip()
        clave_ingresada = self.campo_clave.get().strip()    
        
        if not usuario_ingresado or not clave_ingresada:
            messagebox.showwarning("Atención", "Por favor ingrese su usuario y contraseña.")
        else:
            messagebox.showinfo("Acceso Correcto", f"Bienvenido/a al sistema, {usuario_ingresado}.")
        
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    aplicacion = LoginVentana(ventana_principal)
    ventana_principal.mainloop()