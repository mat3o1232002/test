# interfaz/controles.py
import tkinter as tk
from tkinter import ttk

def crear_controles_ciclo(ciclo, frame):
    widgets = {}
    row_counter = 0
    
    # Parámetros comunes a todos los ciclos
    ttk.Label(frame, text="Flujo másico (kg/s):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
    widgets['flujo_masico'] = ttk.Entry(frame)
    widgets['flujo_masico'].insert(0, "1.0")  # Valor por defecto
    widgets['flujo_masico'].grid(row=row_counter, column=1, padx=5, pady=5)
    row_counter += 1

    ttk.Label(frame, text="Potencia objetivo (kW):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
    widgets['potencia'] = ttk.Entry(frame)
    widgets['potencia'].grid(row=row_counter, column=1, padx=5, pady=5)
    row_counter += 1

    # Parámetros específicos para cada ciclo
    if ciclo == "Rankine con Recalentamiento":
        ttk.Label(frame, text="Presión alta (bar):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['p_alta'] = ttk.Entry(frame)
        widgets['p_alta'].insert(0, "80")  # Valor por defecto
        widgets['p_alta'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Presión baja (bar):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['p_baja'] = ttk.Entry(frame)
        widgets['p_baja'].insert(0, "0.08")  # Valor por defecto
        widgets['p_baja'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Temperatura máxima (°C):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['t_max'] = ttk.Entry(frame)
        widgets['t_max'].insert(0, "500")  # Valor por defecto
        widgets['t_max'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Presión recalentamiento (bar):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['p_media'] = ttk.Entry(frame)
        widgets['p_media'].insert(0, "20")  # Valor por defecto
        widgets['p_media'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Temperatura recalentamiento (°C):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['t_recal'] = ttk.Entry(frame)
        widgets['t_recal'].insert(0, "500")  # Valor por defecto
        widgets['t_recal'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

    elif ciclo == "Brayton con Recalentamiento":
        ttk.Label(frame, text="Relación de compresión:").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['relacion_compresion'] = ttk.Entry(frame)
        widgets['relacion_compresion'].insert(0, "10")  # Valor por defecto
        widgets['relacion_compresion'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Temperatura máxima (°C):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['t_max'] = ttk.Entry(frame)
        widgets['t_max'].insert(0, "950")  # Valor por defecto
        widgets['t_max'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Temperatura recalentamiento (°C):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['t_recal'] = ttk.Entry(frame)
        widgets['t_recal'].insert(0, "950")  # Valor por defecto
        widgets['t_recal'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Pérdida de presión (%):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['p_loss'] = ttk.Entry(frame)
        widgets['p_loss'].insert(0, "5")  # Valor por defecto
        widgets['p_loss'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

    elif ciclo == "Rankine Regenerativo":
        ttk.Label(frame, text="Presión alta (bar):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['p_alta'] = ttk.Entry(frame)
        widgets['p_alta'].insert(0, "80")  # Valor por defecto
        widgets['p_alta'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Presión baja (bar):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['p_baja'] = ttk.Entry(frame)
        widgets['p_baja'].insert(0, "0.08")  # Valor por defecto
        widgets['p_baja'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Temperatura máxima (°C):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['t_max'] = ttk.Entry(frame)
        widgets['t_max'].insert(0, "500")  # Valor por defecto
        widgets['t_max'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Presión extracción (bar):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['p_extraccion'] = ttk.Entry(frame)
        widgets['p_extraccion'].insert(0, "10")  # Valor por defecto
        widgets['p_extraccion'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

    elif ciclo == "Ciclo Otto":
        ttk.Label(frame, text="Relación de compresión:").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['relacion_compresion'] = ttk.Entry(frame)
        widgets['relacion_compresion'].insert(0, "8")  # Valor por defecto
        widgets['relacion_compresion'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Temperatura inicial (°C):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['t1'] = ttk.Entry(frame)
        widgets['t1'].insert(0, "25")  # Valor por defecto
        widgets['t1'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Presión inicial (bar):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['p1'] = ttk.Entry(frame)
        widgets['p1'].insert(0, "1.013")  # Valor por defecto
        widgets['p1'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Temperatura máxima (°C):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['t3'] = ttk.Entry(frame)
        widgets['t3'].insert(0, "1500")  # Valor por defecto
        widgets['t3'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

    elif ciclo == "Ciclo Diesel":
        ttk.Label(frame, text="Relación de compresión:").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['relacion_compresion'] = ttk.Entry(frame)
        widgets['relacion_compresion'].insert(0, "18")  # Valor por defecto
        widgets['relacion_compresion'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Relación de corte:").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['relacion_corte'] = ttk.Entry(frame)
        widgets['relacion_corte'].insert(0, "2")  # Valor por defecto
        widgets['relacion_corte'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Temperatura inicial (°C):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['t1'] = ttk.Entry(frame)
        widgets['t1'].insert(0, "25")  # Valor por defecto
        widgets['t1'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Presión inicial (bar):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['p1'] = ttk.Entry(frame)
        widgets['p1'].insert(0, "1.013")  # Valor por defecto
        widgets['p1'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

    elif ciclo == "Ciclo Carnot":
        ttk.Label(frame, text="Temperatura caliente (°C):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['t_caliente'] = ttk.Entry(frame)
        widgets['t_caliente'].insert(0, "300")  # Valor por defecto
        widgets['t_caliente'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Temperatura fría (°C):").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['t_fria'] = ttk.Entry(frame)
        widgets['t_fria'].insert(0, "50")  # Valor por defecto
        widgets['t_fria'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

        ttk.Label(frame, text="Fuente de calor:").grid(row=row_counter, column=0, padx=5, pady=5, sticky="e")
        widgets['fuente_caliente'] = ttk.Combobox(frame, values=["agua", "vapor"], state="readonly")
        widgets['fuente_caliente'].set("vapor")
        widgets['fuente_caliente'].grid(row=row_counter, column=1, padx=5, pady=5)
        row_counter += 1

    return widgets