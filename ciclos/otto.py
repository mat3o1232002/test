# Módulo para resolver el ciclo Otto
from util.propiedades import PropiedadesTermodinamicas

class CicloOtto:
    def __init__(self):
        self.pt = PropiedadesTermodinamicas("Air")
        self.resultados = {}
    
    def calcular(self, parametros):
        """
        Parámetros obligatorios:
        - relacion_compresion: (V1/V2)
        - t1: Temperatura inicial [°C]
        - p1: Presión inicial [bar]
        - t3: Temperatura máxima [°C]
        
        Opcionales:
        - flujo_masico: [kg/s]
        - potencia: [kW]
        """
        try:
            rc = parametros['relacion_compresion']
            t1 = parametros['t1']
            p1 = parametros['p1']
            t3 = parametros['t3']
            
            flujo_masico = parametros.get('flujo_masico', 1.0)
            
            # 1-2: Compresión isentrópica
            h1 = self.pt.entalpia(p1, t1)
            s1 = self.pt.entropia(p1, t1)
            p2 = p1 * (rc**1.4)
            h2 = self.pt.propiedades_estado(p2, s_kjkgK=s1)['h']
            
            # 2-3: Adición de calor isocórica
            h3 = self.pt.entalpia(p2, t3)
            q_in = h3 - h2
            
            # 3-4: Expansión isentrópica
            s3 = self.pt.entropia(p2, t3)
            p4 = p1
            h4 = self.pt.propiedades_estado(p4, s_kjkgK=s3)['h']
            
            # 4-1: Rechazo de calor
            q_out = h4 - h1
            
            w_neto = q_in - q_out
            
            if 'potencia' in parametros:
                flujo_masico = parametros['potencia'] / w_neto
            
            self.resultados = {
                'Eficiencia térmica': (1 - (1/rc)**0.4) * 100,
                'Trabajo neto': w_neto,
                'Calor añadido': q_in,
                'Presión máxima': p2,
                'Flujo másico': flujo_masico,
                'Potencia neta': w_neto * flujo_masico
            }
            
            return self.formatear_resultados()
            
        except Exception as e:
            raise ValueError(f"Error en cálculo Otto: {str(e)}")
    
    def formatear_resultados(self):
        return {k: f"{v:.2f} {'kJ/kg' if k in ['Trabajo neto', 'Calor añadido'] else ''}" 
                if isinstance(v, float) else v 
                for k, v in self.resultados.items()}

def calcular(parametros):
    return CicloOtto().calcular(parametros)