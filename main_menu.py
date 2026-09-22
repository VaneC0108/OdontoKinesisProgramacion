import tkinter as tk

class PantallaMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="ODONTOKINESIS\nSistema de Gestión", font=("Helvetica", 18, "bold"), pady=20)
        label.pack()

        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Panel Izquierdo: Botonera de navegación
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(side="left", fill="y", padx=20)

        tk.Button(btn_frame, text="Paciente", width=18, height=2, command=lambda: controller.show_frame("PantallaPacientes")).pack(pady=10)
        tk.Button(btn_frame, text="Profesional", width=18, height=2, command=lambda: controller.show_frame("PantallaProfesionales")).pack(pady=10)
        tk.Button(btn_frame, text="Turno", width=18, height=2, command=lambda: controller.show_frame("PantallaTurnos")).pack(pady=10)
        tk.Button(btn_frame, text="Consultas", width=18, height=2, command=lambda: controller.show_frame("PantallaConsultas")).pack(pady=10)
        tk.Button(btn_frame, text="Salir", width=18, height=2, command=self.quit, bg="#f44336", fg="white").pack(pady=10)

        # Panel Derecho: Profesionales del centro
        info_frame = tk.LabelFrame(main_frame, text=" Profesionales del centro ", padx=20, pady=20)
        info_frame.pack(side="right", fill="both", expand=True, padx=20)

        tk.Label(info_frame, text="• Lic. Eliana Roxana Canovas - Kinesióloga", font=("Helvetica", 11), anchor="w").pack(fill="x", pady=10)
        tk.Label(info_frame, text="• Dra. Mariana Rosa Canovas - Odontóloga", font=("Helvetica", 11), anchor="w").pack(fill="x", pady=10)
