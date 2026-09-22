import tkinter as tk
from tkinter import messagebox
 
from estilos import FUENTE_TITULO, FUENTE_SUBTITULO, boton_primario
import modelo_datos as datos
 
 
class MenuPrincipal:
    def __init__(self, ventana, usuario, ventana_login=None):
        self.ventana = ventana
        self.usuario = usuario
        self.ventana_login = ventana_login
 
        self.ventana.title("OdontoKinesis - Sistema de Gestión")
        self.ventana.geometry("600x430")
        self.ventana.resizable(False, False)
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir)
 
        contenedor = tk.Frame(self.ventana, padx=20, pady=20)
        contenedor.pack(fill="both", expand=True)
 
        # --- Panel izquierdo: título + navegación -----------------
        panel_izq = tk.Frame(contenedor)
        panel_izq.pack(side="left", fill="y", padx=(0, 20))
 
        tk.Label(panel_izq, text="ODONTOKINESIS", font=FUENTE_TITULO).pack(anchor="w")
        tk.Label(panel_izq, text="Sistema de Gestión", font=FUENTE_SUBTITULO).pack(
            anchor="w", pady=(0, 20)
        )
 
        boton_primario(panel_izq, "Paciente", self.abrir_pacientes).pack(fill="x", pady=6)
        boton_primario(panel_izq, "Profesional", self.abrir_profesionales).pack(fill="x", pady=6)
        boton_primario(panel_izq, "Turno", self.abrir_turnos).pack(fill="x", pady=6)
        boton_primario(panel_izq, "Consultas", self.abrir_consultas).pack(fill="x", pady=6)
        boton_primario(panel_izq, "Salir", self.salir, bg="#B00020", activebackground="#7F0016").pack(
            fill="x", pady=(20, 6)
        )
 
        # --- Panel derecho: profesionales del centro ---------------
        panel_der = tk.LabelFrame(contenedor, text="Profesionales del centro", padx=10, pady=10)
        panel_der.pack(side="right", fill="both", expand=True)
 
        self.lista_profesionales = tk.Listbox(panel_der, activestyle="none")
        self.lista_profesionales.pack(fill="both", expand=True)
        self._refrescar_profesionales()
 
    def _refrescar_profesionales(self):
        self.lista_profesionales.delete(0, tk.END)
        for prof in datos.profesionales:
            titulo = "Lic." if prof["especialidad"] == "Kinesiología" else "Dra./Dr."
            self.lista_profesionales.insert(
                tk.END,
                f"{titulo} {prof['nombre']} {prof['apellido']} - {prof['especialidad']}",
            )
 
    # --- Navegación a las demás pantallas --------------------------
    def abrir_pacientes(self):
        from pacientes_view import PacientesVentana
        PacientesVentana(tk.Toplevel(self.ventana))
 
    def abrir_profesionales(self):
        from profesionales_view import ProfesionalesVentana
        ProfesionalesVentana(tk.Toplevel(self.ventana), al_cerrar=self._refrescar_profesionales)
 
    def abrir_turnos(self):
        from turnos_view import TurnosVentana
        TurnosVentana(tk.Toplevel(self.ventana))
 
    def abrir_consultas(self):
        from consultas_view import ConsultasVentana
        ConsultasVentana(tk.Toplevel(self.ventana))
 
    def salir(self):
        if messagebox.askyesno("Cerrar sesión", "¿Seguro que querés cerrar sesión y salir?"):
            self.ventana.destroy()
            if self.ventana_login is not None:
                self.ventana_login.deiconify()
            else:
                self.ventana.quit()