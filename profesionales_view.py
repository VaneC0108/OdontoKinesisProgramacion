import tkinter as tk
from tkinter import ttk, messagebox
 
from estilos import FUENTE_SUBTITULO, boton_primario
import modelo_datos as datos
 
 
class ProfesionalesVentana:
    def __init__(self, ventana, al_cerrar=None):
        self.ventana = ventana
        self.al_cerrar = al_cerrar
        self.ventana.title("OdontoKinesis - Gestión de Profesionales")
        self.ventana.geometry("680x520")
        self.ventana.protocol("WM_DELETE_WINDOW", self._cerrar)
 
        self.matricula_seleccionada = None
 
        contenedor = tk.Frame(self.ventana, padx=15, pady=15)
        contenedor.pack(fill="both", expand=True)
 
        marco_datos = tk.LabelFrame(contenedor, text="Datos del Profesional", padx=10, pady=10)
        marco_datos.pack(fill="x")
 
        self.campo_nombre = self._fila_entry(marco_datos, "Nombre", 0)
        self.campo_apellido = self._fila_entry(marco_datos, "Apellido", 1)
        self.combo_especialidad = self._fila_combo(
            marco_datos, "Especialidad", 2, datos.ESPECIALIDADES
        )
        self.campo_matricula = self._fila_entry(marco_datos, "Matricula", 3)
        self.campo_telefono = self._fila_entry(marco_datos, "Teléfono", 4)
        marco_datos.columnconfigure(1, weight=1)
 
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
 
        tk.Label(contenedor, text="Listado de Profesionales", font=FUENTE_SUBTITULO).pack(
            anchor="w", pady=(10, 4)
        )
 
        columnas = ("matricula", "nombre", "apellido", "telefono", "especialidad")
        self.tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", height=8)
        for col, titulo in zip(
            columnas, ["MATRÍCULA", "NOMBRE", "APELLIDO", "TELÉFONO", "ESPECIALIDAD"]
        ):
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=110)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_de_tabla)
 
        self._refrescar_tabla()
 
    def _fila_entry(self, parent, etiqueta, fila):
        tk.Label(parent, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=4)
        entry = tk.Entry(parent)
        entry.grid(row=fila, column=1, sticky="ew", pady=4, padx=(10, 0))
        return entry
 
    def _fila_combo(self, parent, etiqueta, fila, valores):
        tk.Label(parent, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=4)
        combo = ttk.Combobox(parent, values=valores, state="readonly")
        combo.grid(row=fila, column=1, sticky="ew", pady=4, padx=(10, 0))
        return combo
 
    def _refrescar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for p in datos.profesionales:
            self.tabla.insert(
                "", tk.END,
                values=(p["matricula"], p["nombre"], p["apellido"], p["telefono"], p["especialidad"]),
            )
 
    def _seleccionar_de_tabla(self, _evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        matricula, nombre, apellido, telefono, especialidad = self.tabla.item(seleccion[0], "values")
        self.matricula_seleccionada = matricula
        self.campo_matricula.delete(0, tk.END); self.campo_matricula.insert(0, matricula)
        self.campo_nombre.delete(0, tk.END); self.campo_nombre.insert(0, nombre)
        self.campo_apellido.delete(0, tk.END); self.campo_apellido.insert(0, apellido)
        self.campo_telefono.delete(0, tk.END); self.campo_telefono.insert(0, telefono)
        self.combo_especialidad.set(especialidad)
 
    def _leer_formulario(self):
        return {
            "matricula": self.campo_matricula.get().strip(),
            "nombre": self.campo_nombre.get().strip(),
            "apellido": self.campo_apellido.get().strip(),
            "especialidad": self.combo_especialidad.get().strip(),
            "telefono": self.campo_telefono.get().strip(),
        }
 
    def _validar(self, p):
        if not all(p.values()):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return False
        return True
 
    def nuevo(self):
        self.limpiar()
 
    def guardar(self):
        p = self._leer_formulario()
        if not self._validar(p):
            return
        if any(x["matricula"] == p["matricula"] for x in datos.profesionales):
            messagebox.showwarning("Atención", "Ya existe un profesional con esa matrícula.")
            return
        datos.profesionales.append(p)
        self._refrescar_tabla()
        self.limpiar()
        messagebox.showinfo("Éxito", "Profesional guardado correctamente.")
 
    def modificar(self):
        if self.matricula_seleccionada is None:
            messagebox.showwarning("Atención", "Seleccioná un profesional de la tabla para modificar.")
            return
        p = self._leer_formulario()
        if not self._validar(p):
            return
        for i, existente in enumerate(datos.profesionales):
            if existente["matricula"] == self.matricula_seleccionada:
                datos.profesionales[i] = p
                break
        self._refrescar_tabla()
        self.limpiar()
        messagebox.showinfo("Éxito", "Profesional modificado correctamente.")
 
    def eliminar(self):
        if self.matricula_seleccionada is None:
            messagebox.showwarning("Atención", "Seleccioná un profesional de la tabla para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este profesional?"):
            datos.profesionales[:] = [
                x for x in datos.profesionales if x["matricula"] != self.matricula_seleccionada
            ]
            self._refrescar_tabla()
            self.limpiar()
 
    def buscar(self):
        matricula = self.campo_matricula.get().strip()
        if not matricula:
            messagebox.showwarning("Atención", "Ingresá una matrícula para buscar.")
            return
        encontrado = next((x for x in datos.profesionales if x["matricula"] == matricula), None)
        if encontrado is None:
            messagebox.showinfo("Búsqueda", "No se encontró ningún profesional con esa matrícula.")
        else:
            self.matricula_seleccionada = matricula
            self.campo_nombre.delete(0, tk.END); self.campo_nombre.insert(0, encontrado["nombre"])
            self.campo_apellido.delete(0, tk.END); self.campo_apellido.insert(0, encontrado["apellido"])
            self.campo_telefono.delete(0, tk.END); self.campo_telefono.insert(0, encontrado["telefono"])
            self.combo_especialidad.set(encontrado["especialidad"])
 
    def limpiar(self):
        self.matricula_seleccionada = None
        for campo in (self.campo_nombre, self.campo_apellido, self.campo_matricula, self.campo_telefono):
            campo.delete(0, tk.END)
        self.combo_especialidad.set("")
 
    def _cerrar(self):
        if self.al_cerrar:
            self.al_cerrar()
        self.ventana.destroy()
 
 
if __name__ == "__main__":
    raiz = tk.Tk()
    ProfesionalesVentana(raiz)
    raiz.mainloop()