import tkinter as tk
from tkinter import ttk, simpledialog
 
from estilos import boton_primario
import modelo_datos as datos
 
 
class ConsultasVentana:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("OdontoKinesis - Consultas")
        self.ventana.geometry("780x480")
 
        contenedor = tk.Frame(self.ventana, padx=15, pady=15)
        contenedor.pack(fill="both", expand=True)
 
        panel_izq = tk.LabelFrame(contenedor, text="Opciones de Consultas", padx=10, pady=10)
        panel_izq.pack(side="left", fill="y", padx=(0, 15))
 
        opciones = [
            ("Turnos por fecha", self.turnos_por_fecha),
            ("Turnos por profesional", self.turnos_por_profesional),
            ("Turnos por paciente", self.turnos_por_paciente),
            ("Turnos por estado", self.turnos_por_estado),
            ("Cantidad de turnos por profesional", self.cantidad_por_profesional),
        ]
        for texto, comando in opciones:
            boton_primario(panel_izq, texto, comando, wraplength=170).pack(fill="x", pady=4)
 
        panel_der = tk.LabelFrame(contenedor, text="Resultados", padx=10, pady=10)
        panel_der.pack(side="right", fill="both", expand=True)
 
        self.columnas_turno = ("id_turno", "dni_paciente", "matricula_prof", "fecha", "hora", "estado")
        self.tabla = ttk.Treeview(panel_der, columns=self.columnas_turno, show="headings", height=10)
        for col, titulo in zip(
            self.columnas_turno,
            ["ID_Turno", "Paciente (DNI)", "Profesional (Matrícula)", "Fecha", "Hora", "Estado"],
        ):
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=100)
        self.tabla.pack(fill="both", expand=True)
 
        self.etiqueta_info = tk.Label(
            panel_der, text="Los resultados se mostrarán en la tabla según la opción seleccionada."
        )
        self.etiqueta_info.pack(fill="x", pady=(8, 0))
 
    # --- Utilidades de presentación --------------------------------
    def _mostrar_turnos(self, lista, mensaje):
        self._mostrar_columnas_turno()
        self.tabla.delete(*self.tabla.get_children())
        for t in lista:
            self.tabla.insert(
                "", tk.END,
                values=(t["id_turno"], t["dni_paciente"], t["matricula_prof"],
                        t["fecha"], t["hora"], t["estado"]),
            )
        self.etiqueta_info.config(text=f"{mensaje} — {len(lista)} resultado(s).")
 
    def _mostrar_columnas_turno(self):
        self.tabla.config(columns=self.columnas_turno)
        for col, titulo in zip(
            self.columnas_turno,
            ["ID_Turno", "Paciente (DNI)", "Profesional (Matrícula)", "Fecha", "Hora", "Estado"],
        ):
            self.tabla.heading(col, text=titulo)
 
    # --- Las 5 consultas del boceto ---------------------------------
    def turnos_por_fecha(self):
        fecha = simpledialog.askstring("Turnos por fecha", "Ingresá la fecha (dd/mm/aaaa):")
        if fecha is None:
            return
        resultado = [t for t in datos.turnos if t["fecha"] == fecha.strip()]
        self._mostrar_turnos(resultado, f"Turnos en la fecha {fecha}")
 
    def turnos_por_profesional(self):
        matricula = simpledialog.askstring(
            "Turnos por profesional", "Ingresá la matrícula del profesional:"
        )
        if matricula is None:
            return
        resultado = [t for t in datos.turnos if t["matricula_prof"] == matricula.strip()]
        self._mostrar_turnos(resultado, f"Turnos del profesional {matricula}")
 
    def turnos_por_paciente(self):
        dni = simpledialog.askstring("Turnos por paciente", "Ingresá el DNI del paciente:")
        if dni is None:
            return
        resultado = [t for t in datos.turnos if t["dni_paciente"] == dni.strip()]
        self._mostrar_turnos(resultado, f"Turnos del paciente {dni}")
 
    def turnos_por_estado(self):
        estado = simpledialog.askstring(
            "Turnos por estado",
            f"Ingresá el estado ({', '.join(datos.ESTADOS_TURNO)}):",
        )
        if estado is None:
            return
        resultado = [t for t in datos.turnos if t["estado"].lower() == estado.strip().lower()]
        self._mostrar_turnos(resultado, f"Turnos en estado {estado}")
 
    def cantidad_por_profesional(self):
        # Esta consulta agrupa, así que cambiamos las columnas de la tabla.
        conteos = {}
        for t in datos.turnos:
            conteos[t["matricula_prof"]] = conteos.get(t["matricula_prof"], 0) + 1
 
        self.tabla.config(columns=("matricula", "nombre_completo", "cantidad"))
        for col, titulo in zip(
            ("matricula", "nombre_completo", "cantidad"),
            ["MATRÍCULA", "PROFESIONAL", "CANTIDAD DE TURNOS"],
        ):
            self.tabla.heading(col, text=titulo)
 
        self.tabla.delete(*self.tabla.get_children())
        for matricula, cantidad in conteos.items():
            prof = next((p for p in datos.profesionales if p["matricula"] == matricula), None)
            nombre_completo = f"{prof['nombre']} {prof['apellido']}" if prof else "(desconocido)"
            self.tabla.insert("", tk.END, values=(matricula, nombre_completo, cantidad))
 
        self.etiqueta_info.config(
            text=f"Cantidad de turnos por profesional — {len(conteos)} profesional(es) con turnos."
        )
 
 
if __name__ == "__main__":
    raiz = tk.Tk()
    ConsultasVentana(raiz)
    raiz.mainloop()