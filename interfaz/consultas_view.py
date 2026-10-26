import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from interfaz.estilos import boton_primario
from acceso_datos import modelo_datos as datos
from interfaz.errores_ui import mostrar_errores_bd
 
 
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
    @mostrar_errores_bd
    def turnos_por_fecha(self):
        ventana_selector = tk.Toplevel(self.ventana)
        ventana_selector.title("Consultar por Fecha")
        ventana_selector.geometry("300x150")
        
        tk.Label(ventana_selector, text="Ingrese la fecha (dd/mm/aaaa):").pack(pady=10)
        entrada_fecha = tk.Entry(ventana_selector)
        entrada_fecha.pack(pady=5)
        
        def enviar_seleccion():
            fecha_sel = entrada_fecha.get().strip()
            if not fecha_sel:
                messagebox.showwarning("Advertencia", "Debe ingresar una fecha válida.")
                return
            ventana_selector.destroy()
            resultado = datos.obtener_turnos_por_fecha(fecha_sel)
            self.self_mostrar_turnos(resultado, f"Turnos en la fecha {fecha_sel}")
            
        tk.Button(ventana_selector, text="Consultar", command=enviar_seleccion).pack(pady=10)

    @mostrar_errores_bd
    def turnos_por_profesional(self):
        lista_profesionales = datos.obtener_profesionales()
        if not lista_profesionales:
            messagebox.showwarning("Advertencia", "No hay profesionales cargados en el sistema.")
            return
            
        ventana_selector = tk.Toplevel(self.ventana)
        ventana_selector.title("Seleccionar Profesional")
        ventana_selector.geometry("340x160")
        
        tk.Label(ventana_selector, text="Elija un profesional:").pack(pady=10)
        combo = ttk.Combobox(ventana_selector, state="readonly")
        combo['values'] = [f"{p} - {p}, {p}" for p in lista_profesionales]
        combo.pack(pady=5)
        
        def enviar_seleccion():
            if not combo.get():
                messagebox.showwarning("Advertencia", "Por favor, elija un profesional de la lista.")
                return
            partes = combo.get().split(" - ")
            matricula_sel = partes[0].strip()
            ventana_selector.destroy()
            resultado = datos.obtener_turnos_por_profesional(matricula_sel)
            self.mostrar_turnos(resultado, f"Turnos del profesional {combo.get()}")
            
        tk.Button(ventana_selector, text="Consultar", command=enviar_seleccion).pack(pady=10)

    @mostrar_errores_bd
    def turnos_por_paciente(self):
        lista_pacientes = datos.obtener_pacientes()
        if not lista_pacientes:
            messagebox.showwarning("Advertencia", "No hay pacientes cargados en el sistema.")
            return
            
        ventana_selector = tk.Toplevel(self.ventana)
        ventana_selector.title("Seleccionar Paciente")
        ventana_selector.geometry("340x160")
        
        tk.Label(ventana_selector, text="Elija un paciente:").pack(pady=10)
        combo = ttk.Combobox(ventana_selector, state="readonly")
        combo['values'] = [f"{p} - {p}, {p}" for p in lista_pacientes]
        combo.pack(pady=5)
        
        def enviar_seleccion():
            if not combo.get():
                messagebox.showwarning("Advertencia", "Por favor, elija un paciente de la lista.")
                return
            partes = combo.get().split(" - ")
            dni_sel = partes[0].strip()
            ventana_selector.destroy()
            resultado = datos.obtener_turnos_por_paciente(dni_sel)
            self.mostrar_turnos(resultado, f"Turnos del paciente DNI {combo.get()}")
            
        tk.Button(ventana_selector, text="Consultar", command=enviar_seleccion).pack(pady=10)

    @mostrar_errores_bd
    def turnos_por_estado(self):
        ventana_selector = tk.Toplevel(self.ventana)
        ventana_selector.title("Consultar por Estado")
        ventana_selector.geometry("300x150")
        
        tk.Label(ventana_selector, text="Elija un estado de turno:").pack(pady=10)
        combo = ttk.Combobox(ventana_selector, state="readonly")
        combo['values'] = datos.ESTADOS_TURNO
        combo.pack(pady=5)
        
        def enviar_seleccion():
            if not combo.get():
                messagebox.showwarning("Advertencia", "Por favor, elija un estado de la lista.")
                return
            estado_sel = combo.get()
            ventana_selector.destroy()
            resultado = datos.obtener_turnos_por_estado(estado_sel)
            self.self_mostrar_turnos(resultado, f"Turnos con estado {estado_sel}")
            
        tk.Button(ventana_selector, text="Consultar", command=enviar_seleccion).pack(pady=10)
 
    def turnos_por_profesional(self):
        # Obtener la lista de profesionales desde la base de datos
        lista_profesionales = datos.obtener_profesionales() # Asegúrate de que esta función exista en tu modelo de datos
        
        # Si no hay profesionales cargados
        if not lista_profesionales:
            return
            
        # Crear una ventana secundaria para el selector
        ventana_selector = tk.Toplevel(self.ventana)
        ventana_selector.title("Seleccionar Profesional")
        ventana_selector.geometry("300x150")
        
        tk.Label(ventana_selector, text="Elija un profesional:").pack(pady=10)
        
        # Crear el selector (Combobox)
        combo = ttk.Combobox(ventana_selector, state="readonly")
        # Mostrar el formato "Matrícula - Apellido, Nombre"
        combo['values'] = [f"{p[0]} - {p[2]}, {p[1]}" for p in lista_profesionales]
        combo.pack(pady=5)
        combo.current(0)
        
        def enviar_seleccion():
            # Extraer solo la matrícula (lo que está antes del guión)
            matricula_sel = combo.get().split(" - ")[0]
            ventana_selector.destroy()
            resultado = datos.obtener_turnos_por_profesional(matricula_sel.strip())
            self.self_mostrar_turnos(resultado, f"Turnos del profesional {matricula_sel}")
            
        tk.Button(ventana_selector, text="Consultar", command=enviar_seleccion).pack(pady=10)
    def turnos_por_paciente(self):
        # Obtener la lista de pacientes desde la base de datos
        lista_pacientes = datos.obtener_pacientes()
        
        if not lista_pacientes:
            return
            
        ventana_selector = tk.Toplevel(self.ventana)
        ventana_selector.title("Seleccionar Paciente")
        ventana_selector.geometry("300x150")
        
        tk.Label(ventana_selector, text="Elija un paciente:").pack(pady=10)
        
        combo = ttk.Combobox(ventana_selector, state="readonly")
        # Mostrar el formato "DNI - Apellido, Nombre"
        combo['values'] = [f"{p[0]} - {p[1]}, {p[2]}" for p in lista_pacientes]
        combo.pack(pady=5)
        combo.current(0)
        
        def enviar_seleccion():
         if not combo.get():
             messagebox.showwarning("Advertencia", "Por favor, elija un paciente de la lista.")
             return
         partes = combo.get().split(" - ")
         dni_sel = partes[0].strip()
         ventana_selector.destroy()
         resultado = datos.obtener_turnos_por_paciente(dni_sel)
         self.mostrar_turnos(resultado, f"Turnos del paciente DNI {combo.get()}")
            
        tk.Button(ventana_selector, text="Consultar", command=enviar_seleccion).pack(pady=10)
    def turnos_por_estado(self):
        estado = simpledialog.askstring(
            "Turnos por estado",
            f"Ingresá el estado ({', '.join(datos.ESTADOS_TURNO)}):",
        )
        if estado is None:
            return
        resultado = datos.obtener_turnos_por_estado(estado.strip())
        self._mostrar_turnos(resultado, f"Turnos en estado {estado}")
 
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
        
if __name__ == "__main__":
    raiz = tk.Tk()
    ConsultasVentana(raiz)
    raiz.mainloop()
 