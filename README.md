# Sistema de Gestión OdontoKinesis - Módulo de Persistencia y Validación

Este repositorio contiene la solución del sistema de gestión médica adaptado con persistencia de datos en MySQL y validaciones de interfaz de usuario en Tkinter.

## 🛠️ Modificaciones Realizadas (Octubre 2026)

### 1. Control y Gestión de Errores de Base de Datos
* Se implementaron decoradores personalizados @mostrar_errores_bd en el módulo de consultas (consultas_view.py) para capturar de manera segura excepciones de conectividad y sintaxis de SQL, evitando la caída de la aplicación.

### 2. Componentes de Selección Avanzada (Combobox)
* Se reemplazaron las ventanas de entrada de texto manual (simpledialog.askstring) por selectores de lectura limpia (ttk.Combobox) para los campos de *Profesionales, **Pacientes* y *Estados de Turno*.
* Se integraron alertas preventivas mediante messagebox.showwarning para impedir consultas con selecciones vacías.

### 3. Reglas de Validación de Formularios
* Incorporación de funciones privadas de verificación _validar() en las interfaces de pacientes y profesionales.
* Restricción estricta del campo *Teléfono*: validación de longitud (entre 6 y 15 dígitos) y tipo de dato mediante comprobación de cadenas numéricas (.isdigit()).
