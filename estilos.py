 
COLOR_PRIMARIO = "#0288D1"      # azul del botón "Iniciar Sesión" (tu color real)
COLOR_PRIMARIO_HOVER = "#026CA5"
COLOR_TEXTO_BOTON = "#FFFFFF"
COLOR_FONDO = "#FFFFFF"
COLOR_ENCABEZADO_TABLA = "#D9D9D9"
 
FUENTE_TITULO = ("Segoe UI", 20, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 13, "bold")
FUENTE_LABEL = ("Segoe UI", 10)
FUENTE_BOTON = ("Segoe UI", 10, "bold")
 
 
def boton_primario(parent, texto, comando, **kwargs):
    """Crea un tk.Button con el mismo estilo azul que el botón de Login."""
    import tkinter as tk
    return tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=COLOR_PRIMARIO,
        fg=COLOR_TEXTO_BOTON,
        activebackground=COLOR_PRIMARIO_HOVER,
        font=FUENTE_BOTON,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=6,
        **kwargs)