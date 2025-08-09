# Mostrar resultados en una ventana secundaria
# interfaz/resultados.py

from tkinter import ttk, messagebox
import tkinter as tk

def mostrar_resultados(ventana, ciclo, resultados):
    top = tk.Toplevel(ventana)
    top.title(f"Resultados - {ciclo}")
    top.geometry("400x300")
    
    frame = ttk.Frame(top)
    frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    ttk.Label(frame, text=f"Resultados del ciclo {ciclo}", font=('Segoe UI', 12, 'bold')).pack(pady=10)
    
    for clave, valor in resultados.items():
        ttk.Label(frame, text=f"{clave}: {valor}").pack(anchor="w", padx=20, pady=5)
    
    ttk.Button(frame, text="Cerrar", command=top.destroy).pack(pady=20)