# Módulo para resolver el ciclo Rankine regenerativo
from util.propiedades import PropiedadesTermodinamicas

class CicloRankineRegenerativo:
    def __init__(self):
        self.pt = PropiedadesTermodinamicas("Water")
        self.resultados = {}
    
    def calcular(self, parametros):
        """
        Parámetros obligatorios:
        - p_alta: [bar]
        - p_baja: [bar]
        - t_max: [°C]
        - p_extraccion: [bar]
        
        Opcionales:
        - flujo_masico: [kg/s]
        - potencia: [kW]
        - rendimiento_turbina: (0-1)
        """
        try:
            p_alta = parametros['p_alta']
            p_baja = parametros['p_baja']
            t_max = parametros['t_max']
            p_extra = parametros['p_extraccion']
            
            flujo_masico = parametros.get('flujo_masico', 1.0)
            rend_turbina = parametros.get('rendimiento_turbina', 0.85)
            
            # Calcular estados principales
            h1 = self.pt.entalpia(p_alta, 0.01)
            h2 = self.pt.entalpia(p_alta, t_max)
            s2 = self.pt.entropia(p_alta, t_max)
            
            # Extracción (punto 3)
            h3s = self.pt.propiedades_estado(p_extra, s_kjkgK=s2)['h']
            h3 = h2 - rend_turbina*(h2 - h3s)
            
            # Condensación (punto 4)
            h4 = self.pt.entalpia(p_baja, 0.01)
            
            # Calentador abierto
            y = (h1 - h4)/(h3 - h4)  # Fracción de extracción
            
            # Balances de energía
            q_in = h2 - h1
            w_turbina = (h2 - h3) + (1-y)*(h3 - h4)
            w_bomba = (1-y)*(h1 - h4)
            
            eficiencia = (w_turbina - w_bomba)/q_in
            
            if 'potencia' in parametros:
                flujo_masico = parametros['potencia'] / (w_turbina - w_bomba)
            
            self.resultados = {
                'Eficiencia térmica': eficiencia * 100,
                'Fracción extracción': y * 100,
                'Trabajo turbina': w_turbina,
                'Trabajo bomba': w_bomba,
                'Calor añadido': q_in,
                'Flujo másico': flujo_masico,
                'Potencia neta': (w_turbina - w_bomba) * flujo_masico
            }
            
            return self.formatear_resultados()
            
        except Exception as e:
            raise ValueError(f"Error en cálculo Rankine Regenerativo: {str(e)}")
    
    def formatear_resultados(self):
        return {k: f"{v:.2f} {'%' if 'Eficiencia' in k or 'Fracción' in k else 'kJ/kg' if 'Trabajo' in k or 'Calor' in k else ''}" 
                if isinstance(v, float) else v 
                for k, v in self.resultados.items()}

def calcular(parametros):
    return CicloRankineRegenerativo().calcular(parametros)