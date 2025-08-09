import tkinter as tk
from tkinter import ttk, messagebox
from interfaz.controles import crear_controles_ciclo
from interfaz.resultados import mostrar_resultados
from ciclos import (
    rankine,
    rankine_recalentamiento,
    rankine_regenerativo,
    brayton,
    brayton_recalentamiento,
    otto,
    diesel,
    carnot
)

class SimuladorCiclosApp:
    def __init__(self, master):
        self.master = master
        master.title("Simulador de Ciclos Termodinámicos")
        master.geometry("750x650")
        master.configure(bg="#f0f0f0")
        master.resizable(True, True)

        # Configuración de estilos
        self.configurar_estilos()

        # Diccionario de ciclos disponibles
        self.ciclos_disponibles = {
            "Rankine Simple": {
                "funcion": rankine.calcular,
                "descripcion": "Ciclo Rankine básico para plantas de vapor"
            },
            "Rankine con Recalentamiento": {
                "funcion": rankine_recalentamiento.calcular,
                "descripcion": "Rankine con recalentamiento intermedio"
            },
            "Rankine Regenerativo": {
                "funcion": rankine_regenerativo.calcular,
                "descripcion": "Rankine con extracción de vapor para precalentamiento"
            },
            "Brayton Simple": {
                "funcion": brayton.calcular,
                "descripcion": "Ciclo Brayton para turbinas de gas"
            },
            "Brayton con Recalentamiento": {
                "funcion": brayton_recalentamiento.calcular,
                "descripcion": "Brayton con recalentamiento intermedio"
            },
            "Ciclo Otto": {
                "funcion": otto.calcular,
                "descripcion": "Motor de encendido por chispa"
            },
            "Ciclo Diesel": {
                "funcion": diesel.calcular,
                "descripcion": "Motor de encendido por compresión"
            },
            "Ciclo Carnot": {
                "funcion": carnot.calcular,
                "descripcion": "Ciclo teórico de máxima eficiencia"
            }
        }

        # Variables de control
        self.selected_ciclo = tk.StringVar(value=list(self.ciclos_disponibles.keys())[0])
        self.widgets_ciclo = {}

        # Crear interfaz
        self.crear_interfaz()

    def configurar_estilos(self):
        """Configura los estilos visuales de la aplicación"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores y fuentes
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=5)
        self.style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))
        self.style.configure('TCombobox', padding=5)
        self.style.configure('TLabelframe', background='#f0f0f0')
        self.style.configure('TLabelframe.Label', background='#f0f0f0')
        
        # Estilo especial para botón de cálculo
        self.style.map('Calc.TButton',
                      foreground=[('active', 'white'), ('!disabled', 'white')],
                      background=[('active', '#45a049'), ('!disabled', '#4CAF50')])

    def crear_interfaz(self):
        """Construye todos los componentes de la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título y selección de ciclo
        ttk.Label(main_frame, text="Simulador de Ciclos Termodinámicos", 
                 style='Title.TLabel').grid(row=0, column=0, pady=10, columnspan=2)

        ttk.Label(main_frame, text="Seleccione un ciclo:").grid(row=1, column=0, sticky='e', padx=5)
        
        self.combo_ciclos = ttk.Combobox(
            main_frame, 
            textvariable=self.selected_ciclo,
            values=list(self.ciclos_disponibles.keys()),
            state="readonly",
            width=30
        )
        self.combo_ciclos.grid(row=1, column=1, sticky='we', pady=5)
        self.combo_ciclos.bind("<<ComboboxSelected>>", self.actualizar_parametros)

        # Descripción del ciclo
        self.lbl_descripcion = ttk.Label(
            main_frame, 
            text=self.ciclos_disponibles[self.selected_ciclo.get()]["descripcion"],
            wraplength=500,
            justify=tk.LEFT
        )
        self.lbl_descripcion.grid(row=2, column=0, columnspan=2, pady=(0,10))

        # Frame de parámetros
        self.frame_parametros = ttk.LabelFrame(
            main_frame, 
            text="Parámetros del Ciclo",
            padding=(10, 5)
        )
        self.frame_parametros.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        self.frame_parametros.columnconfigure(1, weight=1)

        # Botón de cálculo
        btn_calcular = ttk.Button(
            main_frame, 
            text="Calcular Ciclo", 
            command=self.ejecutar_ciclo,
            style='Calc.TButton'
        )
        btn_calcular.grid(row=4, column=0, columnspan=2, pady=15)

        # Configurar pesos de filas/columnas
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Inicializar controles
        self.actualizar_parametros()

    def actualizar_parametros(self, _=None):
        """Actualiza los controles de parámetros según el ciclo seleccionado"""
        # Limpiar frame de parámetros
        for widget in self.frame_parametros.winfo_children():
            widget.destroy()

        # Actualizar descripción
        ciclo_actual = self.selected_ciclo.get()
        self.lbl_descripcion.config(
            text=self.ciclos_disponibles[ciclo_actual]["descripcion"]
        )

        # Crear nuevos controles
        self.widgets_ciclo = crear_controles_ciclo(
            ciclo_actual, 
            self.frame_parametros
        )

    def ejecutar_ciclo(self):
        """Ejecuta el cálculo del ciclo seleccionado y muestra los resultados"""
        try:
            # Obtener ciclo seleccionado
            ciclo_nombre = self.selected_ciclo.get()
            funcion_calculo = self.ciclos_disponibles[ciclo_nombre]["funcion"]

            # Recoger parámetros del formulario
            parametros = {}
            for nombre, widget in self.widgets_ciclo.items():
                if isinstance(widget, ttk.Entry):
                    valor = widget.get()
                    if valor.replace('.', '', 1).isdigit():  # Verificar si es número
                        parametros[nombre] = float(valor)
                    elif valor:
                        parametros[nombre] = valor
                elif isinstance(widget, ttk.Combobox):
                    parametros[nombre] = widget.get()

            # Ejecutar cálculo
            resultados = funcion_calculo(parametros)

            # Mostrar resultados
            mostrar_resultados(self.master, ciclo_nombre, resultados)

        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Datos inválidos:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error de Cálculo", f"Ocurrió un error:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorCiclosApp(root)
    root.mainloop()