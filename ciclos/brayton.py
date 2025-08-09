from util.propiedades import PropiedadesTermodinamicas
from math import isclose

class CicloBrayton:
    def __init__(self):
        self.pt = PropiedadesTermodinamicas("Air")
        self.resultados = {}
    
    def calcular(self, parametros):
        """
        Calcula ciclo Brayton simple
        Parámetros obligatorios (2 opciones):
        Opción 1:
        - relacion_compresion: Relación de compresión (P2/P1)
        - t_max: Temperatura máxima [°C]
        
        Opción 2:
        - p_alta: Presión alta [bar]
        - p_baja: Presión baja [bar]
        - t_max: Temperatura máxima [°C]
        
        Parámetros opcionales:
        - flujo_masico: Flujo másico [kg/s] (default: 1 kg/s)
        - potencia: Potencia neta [kW] (sobreescribe flujo_masico)
        - rendimiento_compresor: Rendimiento isentrópico (0-1)
        - rendimiento_turbina: Rendimiento isentrópico (0-1)
        """
        try:
            # Determinar relación de compresión
            if 'relacion_compresion' in parametros:
                rc = parametros['relacion_compresion']
                p_baja = 1.01325  # Presión atmosférica estándar
                p_alta = rc * p_baja
            else:
                p_alta = parametros['p_alta']
                p_baja = parametros['p_baja']
                rc = p_alta / p_baja
            
            t_max = parametros['t_max']
            
            # Parámetros opcionales
            flujo_masico = parametros.get('flujo_masico', 1.0)
            rendimiento_compresor = parametros.get('rendimiento_compresor', 1.0)
            rendimiento_turbina = parametros.get('rendimiento_turbina', 1.0)
            
            # 1. Compresión isentrópica (1-2)
            t1 = 25  # Temperatura ambiente
            h1 = self.pt.entalpia(p_baja, t1)
            s1 = self.pt.entropia(p_baja, t1)
            
            h2s = self.pt.propiedades_estado(p_alta, s_kjkgK=s1)['h']
            h2 = h1 + (h2s - h1)/rendimiento_compresor
            w_compresor = h2 - h1
            
            # 2. Adición de calor (2-3)
            h3 = self.pt.entalpia(p_alta, t_max)
            q_in = h3 - h2
            
            # 3. Expansión en turbina (3-4)
            s3 = self.pt.entropia(p_alta, t_max)
            h4s = self.pt.propiedades_estado(p_baja, s_kjkgK=s3)['h']
            h4 = h3 - rendimiento_turbina * (h3 - h4s)
            w_turbina = h3 - h4
            
            # 4. Rechazo de calor (4-1) - Isobárico
            
            # Si se especificó potencia, recalcular flujo másico
            if 'potencia' in parametros:
                potencia = parametros['potencia']
                w_neto = (w_turbina - w_compresor)
                flujo_masico = potencia / w_neto
            
            # Resultados
            self.resultados = {
                'Eficiencia térmica': (w_turbina - w_compresor) / q_in * 100,
                'Trabajo turbina': w_turbina,
                'Trabajo compresor': w_compresor,
                'Calor añadido': q_in,
                'Relación de compresión': rc,
                'Flujo másico': flujo_masico,
                'Potencia neta': (w_turbina - w_compresor) * flujo_masico,
                'Estados termodinámicos': {
                    '1': {'p': p_baja, 'T': t1},
                    '2': {'p': p_alta},
                    '3': {'p': p_alta, 'T': t_max},
                    '4': {'p': p_baja}
                }
            }
            
            return self.formatear_resultados()
            
        except Exception as e:
            raise ValueError(f"Error en cálculo Brayton: {str(e)}")
    
    def formatear_resultados(self):
        return {
            'Eficiencia térmica': f"{self.resultados['Eficiencia térmica']:.2f}%",
            'Trabajo turbina': f"{self.resultados['Trabajo turbina']:.2f} kJ/kg",
            'Trabajo compresor': f"{self.resultados['Trabajo compresor']:.2f} kJ/kg",
            'Calor añadido': f"{self.resultados['Calor añadido']:.2f} kJ/kg",
            'Relación de compresión': f"{self.resultados['Relación de compresión']:.2f}",
            'Flujo másico': f"{self.resultados['Flujo másico']:.3f} kg/s",
            'Potencia neta': f"{self.resultados['Potencia neta']:.3f} kW",
            'Estados termodinámicos': self.resultados['Estados termodinámicos']
        }

def calcular(parametros):
    return CicloBrayton().calcular(parametros)