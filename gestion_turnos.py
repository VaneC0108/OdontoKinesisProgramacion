import tkinter as tk
from tkinter import ttk, messagebox

class PantallaTurnos(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Gestión de Turnos", font=("Helvetica", 16, "bold"), pady=10).pack()

        form = tk.LabelFrame(self, text=" Datos del Turno ", padx=15, pady=10)
        form.pack(fill="x", padx=20, pady=5)

        tk.Label(form, text="Paciente (DNI):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.ent_paciente = ttk.Entry(form)
        self.ent_paciente.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Profesional (Matrícula):").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.ent_prof = ttk.Entry(form)
        self.ent_prof.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form, text="Fecha (AAAA-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.ent_fecha = ttk.Entry(form)
        self.ent_fecha.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Estado:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        # Desplegable Combobox
        self.combo_estado = ttk.Combobox(form, values=["Reservado", "Confirmado", "Atendido", "Cancelado"], state="readonly")
        self.combo_estado.grid(row=1, column=3, padx=5, pady=5)

        btn_box = tk.Frame(form)
        btn_box.grid(row=2, column=0, columnspan=4, pady=10)
        tk.Button(btn_box, text="Agendar Turno", command=self.agendar, bg="#4CAF50", fg="white").pack(side="left", padx=5)

        # Tabla Treeview para visualizar la lista de turnos
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Paciente", "Profesional", "Fecha", "Estado"), show="headings")
        for col in ("ID", "Paciente", "Profesional", "Fecha", "Estado"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        tk.Button(self, text="← Volver al Menú Principal", command=lambda: controller.show_frame("PantallaMenu")).pack(pady=10)

    def agendar(self):
        if not self.ent_paciente.get() or not self.combo_estado.get():
            messagebox.showwarning("Validación", "Complete los campos obligatorios.")
            return
        id_turno = len(self.tree.get_children()) + 1
        self.tree.insert("", "end", values=(id_turno, self.ent_paciente.get(), self.ent_prof.get(), self.ent_fecha.get(), self.combo_estado.get()))
        messagebox.showinfo("Éxito", "Turno registrado correctamente.")
