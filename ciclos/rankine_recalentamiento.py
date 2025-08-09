from util.propiedades import PropiedadesTermodinamicas

class CicloRankineRecalentamiento:
    def __init__(self):
        self.pt = PropiedadesTermodinamicas("Water")
        self.resultados = {}

    def calcular(self, parametros):
        """
        Parámetros obligatorios:
        - p_alta: Presión alta [bar]
        - p_media: Presión recalentamiento [bar]
        - p_baja: Presión baja [bar]
        - t_max: Temperatura máxima [°C]
        - t_recal: Temperatura recalentamiento [°C]
        
        Opcionales:
        - flujo_masico: [kg/s] (default: 1)
        - potencia: [kW]
        - rendimiento_turbina_HP: (0-1)
        - rendimiento_turbina_LP: (0-1)
        - rendimiento_bomba: (0-1)
        """
        try:
            # Parámetros obligatorios
            p_alta = parametros['p_alta']
            p_media = parametros['p_media']
            p_baja = parametros['p_baja']
            t_max = parametros['t_max']
            t_recal = parametros['t_recal']
            
            # Parámetros opcionales
            flujo_masico = parametros.get('flujo_masico', 1.0)
            rend_turb_HP = parametros.get('rendimiento_turbina_HP', 0.85)
            rend_turb_LP = parametros.get('rendimiento_turbina_LP', 0.85)
            rend_bomba = parametros.get('rendimiento_bomba', 0.8)

            # 1-2: Bomba
            h1 = self.pt.entalpia(p_baja, 0.01)
            s1 = self.pt.entropia(p_baja, 0.01)
            h2s = self.pt.propiedades_estado(p_alta, s_kjkgK=s1)['h']
            h2 = h1 + (h2s - h1)/rend_bomba

            # 2-3: Calentamiento en caldera
            h3 = self.pt.entalpia(p_alta, t_max)
            s3 = self.pt.entropia(p_alta, t_max)

            # 3-4: Expansión HP
            h4s = self.pt.propiedades_estado(p_media, s_kjkgK=s3)['h']
            h4 = h3 - rend_turb_HP*(h3 - h4s)

            # 4-5: Recalentamiento
            h5 = self.pt.entalpia(p_media, t_recal)
            s5 = self.pt.entropia(p_media, t_recal)

            # 5-6: Expansión LP
            h6s = self.pt.propiedades_estado(p_baja, s_kjkgK=s5)['h']
            h6 = h5 - rend_turb_LP*(h5 - h6s)

            # 6-1: Condensación
            q_out = h6 - h1

            # Cálculos de energía
            q_in = (h3 - h2) + (h5 - h4)
            w_turb_HP = h3 - h4
            w_turb_LP = h5 - h6
            w_bomba = h2 - h1
            w_neto = (w_turb_HP + w_turb_LP) - w_bomba

            if 'potencia' in parametros:
                flujo_masico = parametros['potencia'] / w_neto

            self.resultados = {
                'Eficiencia térmica': (w_neto / q_in) * 100,
                'Trabajo turbina HP': w_turb_HP,
                'Trabajo turbina LP': w_turb_LP,
                'Trabajo bomba': w_bomba,
                'Calor añadido': q_in,
                'Calor recalentamiento': h5 - h4,
                'Flujo másico': flujo_masico,
                'Potencia neta': w_neto * flujo_masico,
                'Estados': {
                    '1': {'p': p_baja, 'h': h1},
                    '2': {'p': p_alta, 'h': h2},
                    '3': {'p': p_alta, 'h': h3, 'T': t_max},
                    '4': {'p': p_media, 'h': h4},
                    '5': {'p': p_media, 'h': h5, 'T': t_recal},
                    '6': {'p': p_baja, 'h': h6}
                }
            }

            return self.formatear_resultados()

        except Exception as e:
            raise ValueError(f"Error en cálculo Rankine Recalentamiento: {str(e)}")

    def formatear_resultados(self):
        formatted = {k: f"{v:.2f} {self.get_unidad(k)}" 
                    if isinstance(v, (float, int)) else v 
                    for k, v in self.resultados.items()}
        return formatted

    def get_unidad(self, key):
        if 'Eficiencia' in key:
            return '%'
        elif 'Trabajo' in key or 'Calor' in key:
            return 'kJ/kg'
        elif 'Flujo' in key:
            return 'kg/s'
        elif 'Potencia' in key:
            return 'kW'
        return ''

def calcular(parametros):
    return CicloRankineRecalentamiento().calcular(parametros)