# Módulo para resolver el ciclo Diesel
from util.propiedades import PropiedadesTermodinamicas
from math import isclose

class CicloDiesel:
    def __init__(self):
        self.pt_aire = PropiedadesTermodinamicas("Air")
        self.pt_comb = PropiedadesTermodinamicas("Propane")  # Aproximación para diesel
        self.resultados = {}
    
    def calcular(self, parametros):
        """
        Parámetros obligatorios:
        - relacion_compresion: Relación de compresión (V1/V2)
        - relacion_corte: Relación de corte (V3/V2)
        - t1: Temperatura inicial [°C]
        - p1: Presión inicial [bar]
        
        Opcionales:
        - flujo_masico: [kg/s] (default: 1)
        - potencia: [kW] (sobreescribe flujo_masico)
        - rendimiento_combustion: (0-1)
        """
        try:
            # Parámetros obligatorios
            rc = parametros['relacion_compresion']
            rcut = parametros['relacion_corte']
            t1 = parametros['t1']
            p1 = parametros['p1']
            
            # Parámetros opcionales
            flujo_masico = parametros.get('flujo_masico', 1.0)
            rendimiento_comb = parametros.get('rendimiento_combustion', 0.95)
            
            # 1-2: Compresión isentrópica
            h1 = self.pt_aire.entalpia(p1, t1)
            s1 = self.pt_aire.entropia(p1, t1)
            p2 = p1 * (rc**1.4)  # Aprox. para aire
            h2 = self.pt_aire.propiedades_estado(p2, s_kjkgK=s1)['h']
            t2 = self.pt_aire.temperatura(p2, h2)
            
            # 2-3: Combustión isobárica
            p3 = p2
            t3 = t2 * rcut  # Simplificación
            h3 = self.pt_aire.entalpia(p3, t3)
            q_in = h3 - h2
            
            # 3-4: Expansión isentrópica
            s3 = self.pt_aire.entropia(p3, t3)
            p4 = p1
            h4 = self.pt_aire.propiedades_estado(p4, s_kjkgK=s3)['h']
            w_turbina = h3 - h4
            
            # 4-1: Rechazo de calor
            q_out = h4 - h1
            
            # Eficiencia térmica
            w_neto = q_in - q_out
            
            # Ajuste por potencia si se especifica
            if 'potencia' in parametros:
                flujo_masico = parametros['potencia'] / w_neto
            
            self.resultados = {
                'Eficiencia térmica': (w_neto / q_in) * 100,
                'Trabajo neto': w_neto,
                'Calor añadido': q_in,
                'Presión máxima': p2,
                'Temperatura máxima': t3,
                'Flujo másico': flujo_masico,
                'Potencia neta': w_neto * flujo_masico
            }
            
            return self.formatear_resultados()
            
        except Exception as e:
            raise ValueError(f"Error en cálculo Diesel: {str(e)}")
    
    def formatear_resultados(self):
        return {k: f"{v:.2f} {'kJ/kg' if 'Calor' in k or 'Trabajo' in k else ''}" 
                if isinstance(v, float) else v 
                for k, v in self.resultados.items()}

def calcular(parametros):
    return CicloDiesel().calcular(parametros)