# Funciones de conversión
# util/helpers.py - Archivo COMPLETO y CORREGIDO
def kelvin_to_celsius(temp_k):
    """Convertir Kelvin a Celsius"""
    return temp_k - 273.15

def celsius_to_kelvin(temp_c):
    """Convertir Celsius a Kelvin"""
    return temp_c + 273.15

def kPa_to_bar(pressure_kpa):
    """Convertir kPa a bar"""
    return pressure_kpa / 100

def bar_to_kPa(pressure_bar):
    """Convertir bar a kPa"""
    return pressure_bar * 100

def balance_energia(m, h_in, h_out, q=0, w=0):
    """
    Balance de energía: m*(h_in - h_out) + q - w = 0
    Args:
        m: flujo másico (kg/s)
        h_in, h_out: entalpías (kJ/kg)
        q: calor agregado (kW)
        w: trabajo realizado (kW)
    Returns:
        El valor que no fue proporcionado (q o w)
    """
    if q == 0:
        return m * (h_in - h_out) + w
    else:
        return m * (h_in - h_out) + q

def validar_parametros(parametros, requeridos):
    """
    Validar que los parámetros requeridos estén presentes
    """
    faltantes = [p for p in requeridos if p not in parametros]
    if faltantes:
        raise ValueError(f"Parámetros faltantes: {', '.join(faltantes)}")