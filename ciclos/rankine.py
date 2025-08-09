
from util.propiedades import PropiedadesTermodinamicas
from util.helpers import balance_energia
from math import isclose

class CicloRankine:
    def __init__(self):
        self.pt = PropiedadesTermodinamicas("Water")
        self.resultados = {}
    
    def calcular(self, parametros):
        """
        Calcula ciclo Rankine simple
        Parámetros obligatorios:
        - p_alta: Presión alta [bar]
        - p_baja: Presión baja [bar]
        - t_max: Temperatura máxima [°C]
        
        Parámetros opcionales:
        - flujo_masico: Flujo másico [kg/s] (default: 1 kg/s)
        - potencia: Potencia neta [kW] (si se especifica, sobreescribe flujo_masico)
        - rendimiento_turbina: Rendimiento isentrópico turbina (0-1)
        - rendimiento_bomba: Rendimiento isentrópico bomba (0-1)
        """
        try:
            # Parámetros obligatorios
            p_alta = parametros['p_alta']
            p_baja = parametros['p_baja']
            t_max = parametros['t_max']
            
            # Parámetros opcionales con defaults
            flujo_masico = parametros.get('flujo_masico', 1.0)
            rendimiento_turbina = parametros.get('rendimiento_turbina', 1.0)
            rendimiento_bomba = parametros.get('rendimiento_bomba', 1.0)
            
            # 1. Calentamiento en caldera (1-2)
            h1 = self.pt.entalpia(p_alta, 0.01)  # Líquido saturado a p_alta
            h2 = self.pt.entalpia(p_alta, t_max)  # Vapor sobrecalentado
            q_in = h2 - h1
            
            # 2. Expansión en turbina (2-3)
            s2 = self.pt.entropia(p_alta, t_max)
            h3s = self.pt.propiedades_estado(p_baja, s_kjkgK=s2)['h']  # Isentrópico
            h3 = h2 - rendimiento_turbina * (h2 - h3s)
            w_turbina = h2 - h3
            
            # 3. Condensación (3-4)
            h4 = self.pt.entalpia(p_baja, 0.01)  # Líquido saturado a p_baja
            q_out = h3 - h4
            
            # 4. Compresión en bomba (4-1)
            s4 = self.pt.entropia(p_baja, 0.01)
            h1s = self.pt.propiedades_estado(p_alta, s_kjkgK=s4)['h']
            w_bomba_s = h1s - h4
            w_bomba = w_bomba_s / rendimiento_bomba
            h1_real = h4 + w_bomba
            
            # Si se especificó potencia, recalcular flujo másico
            if 'potencia' in parametros:
                potencia = parametros['potencia']
                w_neto = (w_turbina - w_bomba)
                flujo_masico = potencia / w_neto
            
            # Resultados
            self.resultados = {
                'Eficiencia térmica': (w_turbina - w_bomba) / q_in * 100,
                'Trabajo turbina': w_turbina,
                'Trabajo bomba': w_bomba,
                'Calor añadido': q_in,
                'Calor rechazado': q_out,
                'Flujo másico': flujo_masico,
                'Potencia neta': (w_turbina - w_bomba) * flujo_masico,
                'Estado 1': {'h': h1_real, 's': s4, 'p': p_alta, 'T': self.pt.temperatura(p_alta, h1_real)},
                'Estado 2': {'h': h2, 's': s2, 'p': p_alta, 'T': t_max},
                'Estado 3': {'h': h3, 'p': p_baja},
                'Estado 4': {'h': h4, 's': s4, 'p': p_baja, 'T': self.pt.temperatura(p_baja, h4)}
            }
            
            return self.formatear_resultados()
            
        except Exception as e:
            raise ValueError(f"Error en cálculo Rankine: {str(e)}")
    
    def formatear_resultados(self):
        return {
            'Eficiencia térmica': f"{self.resultados['Eficiencia térmica']:.2f}%",
            'Trabajo turbina': f"{self.resultados['Trabajo turbina']:.2f} kJ/kg",
            'Trabajo bomba': f"{self.resultados['Trabajo bomba']:.2f} kJ/kg",
            'Calor añadido': f"{self.resultados['Calor añadido']:.2f} kJ/kg",
            'Calor rechazado': f"{self.resultados['Calor rechazado']:.2f} kJ/kg",
            'Flujo másico': f"{self.resultados['Flujo másico']:.3f} kg/s",
            'Potencia neta': f"{self.resultados['Potencia neta']:.3f} kW",
            'Estados termodinámicos': self.resultados['Estado 1'] | self.resultados['Estado 2'] | self.resultados['Estado 3'] | self.resultados['Estado 4']
        }

def calcular(parametros):
    return CicloRankine().calcular(parametros)