import tkinter as tk
from tkinter import ttk, messagebox
import re
 
from estilos import FUENTE_SUBTITULO, boton_primario
import modelo_datos as datos
 
 
class TurnosVentana:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("OdontoKinesis - Gestión de Turno")
        self.ventana.geometry("720x560")
 
        self.id_seleccionado = None
 
        contenedor = tk.Frame(self.ventana, padx=15, pady=15)
        contenedor.pack(fill="both", expand=True)
 
        marco_datos = tk.LabelFrame(contenedor, text="Datos del Turno", padx=10, pady=10)
        marco_datos.pack(fill="x")
 
        # columna izquierda: paciente / profesional
        tk.Label(marco_datos, text="Paciente (DNI):").grid(row=0, column=0, sticky="w", pady=4)
        self.combo_paciente = ttk.Combobox(marco_datos, state="readonly")
        self.combo_paciente.grid(row=0, column=1, sticky="ew", padx=(10, 30), pady=4)
 
        tk.Label(marco_datos, text="Profesional Matrícula:").grid(row=1, column=0, sticky="w", pady=4)
        self.combo_profesional = ttk.Combobox(marco_datos, state="readonly")
        self.combo_profesional.grid(row=1, column=1, sticky="ew", padx=(10, 30), pady=4)
 
        # columna derecha: fecha / hora / estado
        tk.Label(marco_datos, text="Fecha (dd/mm/aaaa):").grid(row=0, column=2, sticky="w", pady=4)
        self.campo_fecha = tk.Entry(marco_datos)
        self.campo_fecha.grid(row=0, column=3, sticky="ew", pady=4)
 
        tk.Label(marco_datos, text="Hora (hh:mm):").grid(row=1, column=2, sticky="w", pady=4)
        self.campo_hora = tk.Entry(marco_datos)
        self.campo_hora.grid(row=1, column=3, sticky="ew", pady=4)
 
        tk.Label(marco_datos, text="Estado:").grid(row=2, column=2, sticky="w", pady=4)
        self.combo_estado = ttk.Combobox(marco_datos, values=datos.ESTADOS_TURNO, state="readonly")
        self.combo_estado.grid(row=2, column=3, sticky="ew", pady=4)
 
        marco_datos.columnconfigure(1, weight=1)
        marco_datos.columnconfigure(3, weight=1)
 
        marco_botones = tk.Frame(contenedor)
        marco_botones.pack(fill="x", pady=10)
        for texto, comando in [
            ("Nuevo", self.nuevo),
            ("Guardar", self.guardar),
            ("Modificar", self.modificar),
            ("Eliminar", self.eliminar),
            ("Buscar", self.buscar),
            ("Limpiar", self.limpiar),
        ]:
            boton_primario(marco_botones, texto, comando).pack(side="left", padx=4)
 
        tk.Label(contenedor, text="Listado de Turno", font=FUENTE_SUBTITULO).pack(
            anchor="w", pady=(10, 4)
        )
 
        columnas = ("id_turno", "dni_paciente", "matricula_prof", "fecha", "hora", "estado")
        self.tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", height=8)
        for col, titulo in zip(
            columnas, ["ID_Turno", "Paciente (DNI)", "Profesional (Matrícula)", "Fecha", "Hora", "Estado"]
        ):
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=100)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_de_tabla)
 
        self._cargar_combos()
        self._refrescar_tabla()
 
    # --- Carga de combos desde pacientes/profesionales ya registrados
    def _cargar_combos(self):
        self.combo_paciente["values"] = [p["dni"] for p in datos.pacientes]
        self.combo_profesional["values"] = [p["matricula"] for p in datos.profesionales]
 
    def _refrescar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for t in datos.turnos:
            self.tabla.insert(
                "", tk.END,
                values=(t["id_turno"], t["dni_paciente"], t["matricula_prof"],
                        t["fecha"], t["hora"], t["estado"]),
            )
 
    def _seleccionar_de_tabla(self, _evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        id_turno, dni, matricula, fecha, hora, estado = self.tabla.item(seleccion[0], "values")
        self.id_seleccionado = int(id_turno)
        self.combo_paciente.set(dni)
        self.combo_profesional.set(matricula)
        self.campo_fecha.delete(0, tk.END); self.campo_fecha.insert(0, fecha)
        self.campo_hora.delete(0, tk.END); self.campo_hora.insert(0, hora)
        self.combo_estado.set(estado)
 
    @staticmethod
    def _fecha_valida(fecha):
        return re.match(r"^\d{2}/\d{2}/\d{4}$", fecha) is not None
 
    @staticmethod
    def _hora_valida(hora):
        return re.match(r"^([01]\d|2[0-3]):[0-5]\d$", hora) is not None
 
    def _leer_formulario(self):
        return {
            "dni_paciente": self.combo_paciente.get().strip(),
            "matricula_prof": self.combo_profesional.get().strip(),
            "fecha": self.campo_fecha.get().strip(),
            "hora": self.campo_hora.get().strip(),
            "estado": self.combo_estado.get().strip(),
        }
 
    def _validar(self, t, ignorar_id=None):
        if not all(t.values()):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return False
        if not self._fecha_valida(t["fecha"]):
            messagebox.showwarning("Atención", "La fecha debe tener el formato dd/mm/aaaa.")
            return False
        if not self._hora_valida(t["hora"]):
            messagebox.showwarning("Atención", "La hora debe tener el formato hh:mm (24 hs).")
            return False
        # Regla de negocio: no dos turnos para el mismo profesional en la misma franja
        choque = any(
            x["matricula_prof"] == t["matricula_prof"]
            and x["fecha"] == t["fecha"]
            and x["hora"] == t["hora"]
            and x["id_turno"] != ignorar_id
            for x in datos.turnos
        )
        if choque:
            messagebox.showwarning(
                "Atención", "Ese profesional ya tiene un turno agendado en esa fecha y hora."
            )
            return False
        return True
 
    def nuevo(self):
        self.limpiar()
 
    def guardar(self):
        t = self._leer_formulario()
        if not self._validar(t):
            return
        t["id_turno"] = datos.proximo_id_turno()
        datos.turnos.append(t)
        self._refrescar_tabla()
        self.limpiar()
        messagebox.showinfo("Éxito", "Turno guardado correctamente.")
 
    def modificar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccioná un turno de la tabla para modificar.")
            return
        t = self._leer_formulario()
        if not self._validar(t, ignorar_id=self.id_seleccionado):
            return
        for i, existente in enumerate(datos.turnos):
            if existente["id_turno"] == self.id_seleccionado:
                t["id_turno"] = self.id_seleccionado
                datos.turnos[i] = t
                break
        self._refrescar_tabla()
        self.limpiar()
        messagebox.showinfo("Éxito", "Turno modificado correctamente.")
 
    def eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccioná un turno de la tabla para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este turno?"):
            datos.turnos[:] = [x for x in datos.turnos if x["id_turno"] != self.id_seleccionado]
            self._refrescar_tabla()
            self.limpiar()
 
    def buscar(self):
        dni = self.combo_paciente.get().strip()
        if not dni:
            messagebox.showwarning("Atención", "Seleccioná un paciente para buscar sus turnos.")
            return
        encontrados = [x for x in datos.turnos if x["dni_paciente"] == dni]
        self.tabla.delete(*self.tabla.get_children())
        for t in encontrados:
            self.tabla.insert(
                "", tk.END,
                values=(t["id_turno"], t["dni_paciente"], t["matricula_prof"],
                        t["fecha"], t["hora"], t["estado"]),
            )
        if not encontrados:
            messagebox.showinfo("Búsqueda", "Ese paciente no tiene turnos registrados.")
 
    def limpiar(self):
        self.id_seleccionado = None
        self.combo_paciente.set("")
        self.combo_profesional.set("")
        self.combo_estado.set("")
        self.campo_fecha.delete(0, tk.END)
        self.campo_hora.delete(0, tk.END)
        self._cargar_combos()
        self._refrescar_tabla()
 
 
if __name__ == "__main__":
    raiz = tk.Tk()
    TurnosVentana(raiz)
    raiz.mainloop()