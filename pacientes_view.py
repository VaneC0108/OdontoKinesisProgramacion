import re
import tkinter as tk
from tkinter import ttk, messagebox
 
from estilos import FUENTE_SUBTITULO, boton_primario
import modelo_datos as datos
 
 
class PacientesVentana:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("OdontoKinesis - Gestión de Pacientes")
        self.ventana.geometry("650x520")
 
        self.dni_seleccionado = None  # None = modo "nuevo"
 
        contenedor = tk.Frame(self.ventana, padx=15, pady=15)
        contenedor.pack(fill="both", expand=True)
 
        # --- Formulario ------------------------------------------------
        marco_datos = tk.LabelFrame(contenedor, text="Datos del paciente", padx=10, pady=10)
        marco_datos.pack(fill="x")
 
        self.campo_nombre = self._fila_entry(marco_datos, "Nombre", 0)
        self.campo_apellido = self._fila_entry(marco_datos, "Apellido", 1)
        self.campo_dni = self._fila_entry(marco_datos, "DNI", 2)
        self.campo_telefono = self._fila_entry(marco_datos, "Teléfono", 3)
        self.campo_email = self._fila_entry(marco_datos, "E-Mail", 4)
        marco_datos.columnconfigure(1, weight=1)
 
        # --- Botonera ----------------------------------------------------
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
 
        # --- Listado -------------------------------------------------
        tk.Label(contenedor, text="Listado de pacientes", font=FUENTE_SUBTITULO).pack(
            anchor="w", pady=(10, 4)
        )
 
        columnas = ("dni", "nombre", "apellido", "telefono", "email")
        self.tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", height=8)
        for col, titulo in zip(columnas, ["DNI", "NOMBRE", "APELLIDO", "TELÉFONO", "E-MAIL"]):
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=110)
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_de_tabla)
 
        self._refrescar_tabla()
 
    # --- Helpers de layout -------------------------------------------------
    def _fila_entry(self, parent, etiqueta, fila):
        tk.Label(parent, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=4)
        entry = tk.Entry(parent)
        entry.grid(row=fila, column=1, sticky="ew", pady=4, padx=(10, 0))
        return entry
 
    def _refrescar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for p in datos.pacientes:
            self.tabla.insert(
                "", tk.END,
                values=(p["dni"], p["nombre"], p["apellido"], p["telefono"], p["email"]),
            )
 
    def _seleccionar_de_tabla(self, _evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        dni, nombre, apellido, telefono, email = self.tabla.item(seleccion[0], "values")
        self.dni_seleccionado = dni
        self.campo_dni.delete(0, tk.END); self.campo_dni.insert(0, dni)
        self.campo_nombre.delete(0, tk.END); self.campo_nombre.insert(0, nombre)
        self.campo_apellido.delete(0, tk.END); self.campo_apellido.insert(0, apellido)
        self.campo_telefono.delete(0, tk.END); self.campo_telefono.insert(0, telefono)
        self.campo_email.delete(0, tk.END); self.campo_email.insert(0, email)
 
    # --- Validaciones ------------------------------------------------
    @staticmethod
    def _dni_valido(dni):
        return dni.isdigit() and 6 <= len(dni) <= 10
 
    @staticmethod
    def _email_valido(email):
        return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None
 
    def _leer_formulario(self):
        return {
            "dni": self.campo_dni.get().strip(),
            "nombre": self.campo_nombre.get().strip(),
            "apellido": self.campo_apellido.get().strip(),
            "telefono": self.campo_telefono.get().strip(),
            "email": self.campo_email.get().strip(),
        }
 
    def _validar(self, p):
        if not all([p["dni"], p["nombre"], p["apellido"], p["telefono"], p["email"]]):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return False
        if not self._dni_valido(p["dni"]):
            messagebox.showwarning("Atención", "El DNI debe contener solo números (6 a 10 dígitos).")
            return False
        if not self._email_valido(p["email"]):
            messagebox.showwarning("Atención", "El correo electrónico no es válido.")
            return False
        return True
 
    # --- Acciones de la botonera --------------------------------------
    def nuevo(self):
        self.limpiar()
 
    def guardar(self):
        p = self._leer_formulario()
        if not self._validar(p):
            return
        if any(x["dni"] == p["dni"] for x in datos.pacientes):
            messagebox.showwarning("Atención", "Ya existe un paciente con ese DNI.")
            return
        datos.pacientes.append(p)
        self._refrescar_tabla()
        self.limpiar()
        messagebox.showinfo("Éxito", "Paciente guardado correctamente.")
 
    def modificar(self):
        if self.dni_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccioná un paciente de la tabla para modificar.")
            return
        p = self._leer_formulario()
        if not self._validar(p):
            return
        for i, existente in enumerate(datos.pacientes):
            if existente["dni"] == self.dni_seleccionado:
                datos.pacientes[i] = p
                break
        self._refrescar_tabla()
        self.limpiar()
        messagebox.showinfo("Éxito", "Paciente modificado correctamente.")
 
    def eliminar(self):
        if self.dni_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccioná un paciente de la tabla para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este paciente?"):
            datos.pacientes[:] = [x for x in datos.pacientes if x["dni"] != self.dni_seleccionado]
            self._refrescar_tabla()
            self.limpiar()
 
    def buscar(self):
        dni = self.campo_dni.get().strip()
        if not dni:
            messagebox.showwarning("Atención", "Ingresá un DNI para buscar.")
            return
        encontrado = next((x for x in datos.pacientes if x["dni"] == dni), None)
        if encontrado is None:
            messagebox.showinfo("Búsqueda", "No se encontró ningún paciente con ese DNI.")
        else:
            self.dni_seleccionado = dni
            self.campo_nombre.delete(0, tk.END); self.campo_nombre.insert(0, encontrado["nombre"])
            self.campo_apellido.delete(0, tk.END); self.campo_apellido.insert(0, encontrado["apellido"])
            self.campo_telefono.delete(0, tk.END); self.campo_telefono.insert(0, encontrado["telefono"])
            self.campo_email.delete(0, tk.END); self.campo_email.insert(0, encontrado["email"])
 
    def limpiar(self):
        self.dni_seleccionado = None
        for campo in (self.campo_nombre, self.campo_apellido, self.campo_dni,
                      self.campo_telefono, self.campo_email):
            campo.delete(0, tk.END)
 
 
if __name__ == "__main__":
    raiz = tk.Tk()
    PacientesVentana(raiz)
    raiz.mainloop()