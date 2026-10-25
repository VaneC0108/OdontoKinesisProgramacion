import tkinter as tk
from tkinter import ttk, messagebox
from acceso_datos.reportes import (
    turnos_con_nombres,
    turnos_por_especialidad,
    turnos_por_estado,
    pacientes_sin_turnos
)

class ReportesView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reportes del Sistema - OdontoKinesis")
        self.geometry("850x500")
        
        # Título principal
        titulo = ttk.Label(self, text="Panel de Reportes Avanzados", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        # Botones para seleccionar el reporte
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=5)

        btn1 = ttk.Button(frame_botones, text="Turnos con Pacientes y Profesionales", command=self.mostrar_turnos_completos)
        btn1.grid(row=0, column=0, padx=5, pady=5)

        btn2 = ttk.Button(frame_botones, text="Turnos por Especialidad", command=self.mostrar_por_especialidad)
        btn2.grid(row=0, column=1, padx=5, pady=5)

        btn3 = ttk.Button(frame_botones, text="Turnos por Estado", command=self.mostrar_por_estado)
        btn3.grid(row=1, column=0, padx=5, pady=5)

        btn4 = ttk.Button(frame_botones, text="Pacientes Sin Turnos", command=self.mostrar_pacientes_sin_turnos)
        btn4.grid(row=1, column=1, padx=5, pady=5)

        # Tabla (Treeview) para mostrar los datos
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def mostrar_datos(self, columnas, filas):
        self.limpiar_tabla()
        self.tree["columns"] = columnas
        self.tree["show"] = "headings"

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)

        for fila in filas:
            self.tree.insert("", tk.END, values=fila)

    def mostrar_turnos_completos(self):
        try:
            datos = turnos_con_nombres()
            columnas = ("ID Turno", "Paciente", "Profesional", "Fecha", "Hora", "Estado")
            self.mostrar_datos(columnas, datos)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def mostrar_por_especialidad(self):
        try:
            datos = turnos_por_especialidad()
            columnas = ("Especialidad", "Cantidad de Turnos")
            self.mostrar_datos(columnas, datos)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def mostrar_por_estado(self):
        try:
            datos = turnos_por_estado()
            columnas = ("Estado del Turno", "Cantidad")
            self.mostrar_datos(columnas, datos)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def mostrar_pacientes_sin_turnos(self):
        try:
            datos = pacientes_sin_turnos()
            columnas = ("DNI", "Nombre", "Apellido")
            self.mostrar_datos(columnas, datos)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")