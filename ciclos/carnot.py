# Módulo para resolver el ciclo Carnot de vapor
# ciclos/carnot.py

from util.helpers import kelvin_to_celsius, celsius_to_kelvin
from util.propiedades import PropiedadesTermodinamicas



class CicloCarnot:
    def __init__(self):
        self.pt = PropiedadesTermodinamicas("Water")
    
    def calcular(self, parametros):
        try:
            t_caliente = parametros['t_caliente']
            t_fria = parametros['t_fria']
            
            # Conversión a Kelvin para los cálculos
            t_cal_k = celsius_to_kelvin(t_caliente)
            t_fria_k = celsius_to_kelvin(t_fria)
            
            # Cálculo de eficiencia teórica
            eficiencia = 1 - (t_fria_k / t_cal_k)
            
            return {
                'Eficiencia teórica': f"{eficiencia * 100:.2f}%",
                'Temperatura caliente': f"{t_caliente:.2f} °C",
                'Temperatura fría': f"{t_fria:.2f} °C"
            }
            
        except Exception as e:
            raise ValueError(f"Error en cálculo Carnot: {str(e)}")

def calcular(parametros):
    return CicloCarnot().calcular(parametros)