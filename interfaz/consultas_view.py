
import tkinter as tk
from tkinter import ttk, messagebox
 
from interfaz.errores_ui import mostrar_errores_bd
from interfaz.estilos import boton_primario
from acceso_datos import modelo_datos as datos
 
 
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
        self._mostrar_columnas_turno()
        self.tabla.pack(fill="both", expand=True)
 
        self.etiqueta_info = tk.Label(
            panel_der, text="Los resultados se mostrarán en la tabla según la opción seleccionada."
        )
        self.etiqueta_info.pack(fill="x", pady=(8, 0))
 
    # --- Utilidades de presentación --------------------------------
    def _mostrar_columnas_turno(self):
        self.tabla.config(columns=self.columnas_turno)
        for col, titulo in zip(
            self.columnas_turno,
            ["ID_Turno", "Paciente (DNI)", "Profesional (Matrícula)", "Fecha", "Hora", "Estado"],
        ):
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=100)
 
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
 
    def _abrir_selector(self, titulo, etiqueta, opciones, consultar):
        """Abre una ventanita con una lista desplegable.
 
        'opciones' es una lista de (texto, valor): se muestra el texto y, al
        apretar Consultar, se llama a consultar(valor, texto) con la opción elegida.
        """
        ventana_selector = tk.Toplevel(self.ventana)
        ventana_selector.title(titulo)
        ventana_selector.geometry("340x160")
 
        tk.Label(ventana_selector, text=etiqueta).pack(pady=10)
        combo = ttk.Combobox(
            ventana_selector, state="readonly", width=38,
            values=[texto for texto, _valor in opciones],
        )
        combo.pack(pady=5)
 
        # El decorador va acá adentro porque esta función se ejecuta cuando se
        # aprieta el botón, no cuando se abre la ventanita.
        @mostrar_errores_bd
        def enviar_seleccion():
            if combo.current() < 0:
                messagebox.showwarning("Advertencia", "Por favor, elija una opción de la lista.")
                return
            texto, valor = opciones[combo.current()]
            ventana_selector.destroy()
            consultar(valor, texto)
 
        tk.Button(ventana_selector, text="Consultar", command=enviar_seleccion).pack(pady=10)
 
    # --- Las 5 consultas ---------------------------------------------
    @mostrar_errores_bd
    def turnos_por_fecha(self):
        ventana_selector = tk.Toplevel(self.ventana)
        ventana_selector.title("Consultar por Fecha")
        ventana_selector.geometry("300x150")
 
        tk.Label(ventana_selector, text="Ingrese la fecha (dd/mm/aaaa):").pack(pady=10)
        entrada_fecha = tk.Entry(ventana_selector)
        entrada_fecha.pack(pady=5)
 
        @mostrar_errores_bd
        def enviar_seleccion():
            fecha = entrada_fecha.get().strip()
            if not fecha:
                messagebox.showwarning("Advertencia", "Debe ingresar una fecha.")
                return
            # Si la fecha es inválida, se muestra el aviso y la ventanita queda
            # abierta para corregirla (por eso se cierra recién después).
            resultado = datos.obtener_turnos_por_fecha(fecha)
            ventana_selector.destroy()
            self._mostrar_turnos(resultado, f"Turnos en la fecha {fecha}")
 
        tk.Button(ventana_selector, text="Consultar", command=enviar_seleccion).pack(pady=10)
 
    @mostrar_errores_bd
    def turnos_por_profesional(self):
        profesionales = datos.obtener_profesionales()
        if not profesionales:
            messagebox.showwarning("Advertencia", "No hay profesionales cargados en el sistema.")
            return
        # Se muestra "Matrícula - Apellido, Nombre" y se consulta por la matrícula.
        opciones = [
            (f"{p['matricula']} - {p['apellido']}, {p['nombre']}", p["matricula"])
            for p in profesionales
        ]
        self._abrir_selector(
            "Seleccionar Profesional", "Elija un profesional:", opciones,
            lambda valor, texto: self._mostrar_turnos(
                datos.obtener_turnos_por_profesional(valor), f"Turnos del profesional {texto}"
            ),
        )
 
    @mostrar_errores_bd
    def turnos_por_paciente(self):
        pacientes = datos.obtener_pacientes()
        if not pacientes:
            messagebox.showwarning("Advertencia", "No hay pacientes cargados en el sistema.")
            return
        # Se muestra "DNI - Apellido, Nombre" y se consulta por el DNI.
        opciones = [
            (f"{p['dni']} - {p['apellido']}, {p['nombre']}", p["dni"])
            for p in pacientes
        ]
        self._abrir_selector(
            "Seleccionar Paciente", "Elija un paciente:", opciones,
            lambda valor, texto: self._mostrar_turnos(
                datos.obtener_turnos_por_paciente(valor), f"Turnos del paciente {texto}"
            ),
        )
 
    @mostrar_errores_bd
    def turnos_por_estado(self):
        opciones = [(estado, estado) for estado in datos.ESTADOS_TURNO]
        self._abrir_selector(
            "Consultar por Estado", "Elija un estado de turno:", opciones,
            lambda valor, texto: self._mostrar_turnos(
                datos.obtener_turnos_por_estado(valor), f"Turnos con estado {texto}"
            ),
        )
 
    @mostrar_errores_bd
    def cantidad_por_profesional(self):
        # Esta consulta agrupa, así que cambiamos las columnas de la tabla.
        conteos = datos.obtener_cantidad_turnos_por_profesional()
 
        self.tabla.config(columns=("matricula", "nombre_completo", "cantidad"))
        for col, titulo in zip(
            ("matricula", "nombre_completo", "cantidad"),
            ["MATRÍCULA", "PROFESIONAL", "CANTIDAD DE TURNOS"],
        ):
            self.tabla.heading(col, text=titulo)
 
        self.tabla.delete(*self.tabla.get_children())
        for matricula, cantidad in conteos.items():
            prof = datos.obtener_profesional_por_matricula(matricula)
            nombre_completo = f"{prof['nombre']} {prof['apellido']}" if prof else "(desconocido)"
            self.tabla.insert("", tk.END, values=(matricula, nombre_completo, cantidad))
 
        self.etiqueta_info.config(
            text=f"Cantidad de turnos por profesional — {len(conteos)} profesional(es) con turnos."
        )