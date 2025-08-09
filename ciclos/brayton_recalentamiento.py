from util.propiedades import PropiedadesTermodinamicas

class CicloBraytonRecalentamiento:
    def __init__(self):
        self.pt = PropiedadesTermodinamicas("Air")
        self.resultados = {}

    def calcular(self, parametros):
        """
        Parámetros obligatorios:
        - relacion_compresion: (P2/P1)
        - t_max: Temperatura máxima [°C]
        - t_recal: Temperatura recalentamiento [°C]
        
        Opcionales:
        - flujo_masico: [kg/s] (default: 1)
        - potencia: [kW]
        - rendimiento_compresor: (0-1)
        - rendimiento_turbina_HP: (0-1)
        - rendimiento_turbina_LP: (0-1)
        - p_loss: Pérdida de presión [%] (default: 5)
        """
        try:
            # Parámetros obligatorios
            rc = parametros['relacion_compresion']
            t_max = parametros['t_max']
            t_recal = parametros['t_recal']
            
            # Parámetros opcionales
            flujo_masico = parametros.get('flujo_masico', 1.0)
            rend_comp = parametros.get('rendimiento_compresor', 0.85)
            rend_turb_HP = parametros.get('rendimiento_turbina_HP', 0.9)
            rend_turb_LP = parametros.get('rendimiento_turbina_LP', 0.9)
            p_loss = 1 - (parametros.get("p_loss", 5) / 100) 

            # 1-2: Compresión
            p1 = 1.01325  # bar (estándar)
            t1 = 25  # °C
            h1 = self.pt.entalpia(p1, t1)
            s1 = self.pt.entropia(p1, t1)
            
            p2 = p1 * rc
            h2s = self.pt.propiedades_estado(p2, s_kjkgK=s1)['h']
            h2 = h1 + (h2s - h1)/rend_comp

            # 2-3: Combustión (1ra etapa)
            p3 = p2 * p_loss  # Pérdida de presión
            h3 = self.pt.entalpia(p3, t_max)
            q_in1 = h3 - h2

            # 3-4: Expansión HP
            s3 = self.pt.entropia(p3, t_max)
            p4 = p1 * (rc**0.5)  # Presión intermedia
            h4s = self.pt.propiedades_estado(p4, s_kjkgK=s3)['h']
            h4 = h3 - rend_turb_HP*(h3 - h4s)

            # 4-5: Recalentamiento
            p5 = p4 * p_loss
            h5 = self.pt.entalpia(p5, t_recal)
            q_in2 = h5 - h4

            # 5-6: Expansión LP
            s5 = self.pt.entropia(p5, t_recal)
            p6 = p1
            h6s = self.pt.propiedades_estado(p6, s_kjkgK=s5)['h']
            h6 = h5 - rend_turb_LP*(h5 - h6s)

            # Cálculos de energía
            w_comp = h2 - h1
            w_turb_HP = h3 - h4
            w_turb_LP = h5 - h6
            w_neto = (w_turb_HP + w_turb_LP) - w_comp
            q_in = q_in1 + q_in2

            if 'potencia' in parametros:
                flujo_masico = parametros['potencia'] / w_neto

            self.resultados = {
                'Eficiencia térmica': (w_neto / q_in) * 100,
                'Trabajo compresor': w_comp,
                'Trabajo turbina HP': w_turb_HP,
                'Trabajo turbina LP': w_turb_LP,
                'Calor añadido': q_in,
                'Relación de compresión': rc,
                'Flujo másico': flujo_masico,
                'Potencia neta': w_neto * flujo_masico,
                'Estados': {
                    '1': {'p': p1, 'T': t1},
                    '2': {'p': p2},
                    '3': {'p': p3, 'T': t_max},
                    '4': {'p': p4},
                    '5': {'p': p5, 'T': t_recal},
                    '6': {'p': p6}
                }
            }

            return self.formatear_resultados()

        except Exception as e:
            raise ValueError(f"Error en cálculo Brayton Recalentamiento: {str(e)}")

    def formatear_resultados(self):
        units = {
            'Eficiencia': '%',
            'Trabajo': 'kJ/kg',
            'Calor': 'kJ/kg',
            'Flujo': 'kg/s',
            'Potencia': 'kW',
            'Relación': ''
        }
        
        formatted = {}
        for k, v in self.resultados.items():
            if isinstance(v, dict):
                formatted[k] = v
            else:
                unit = next((u for key, u in units.items() if key in k), '')
                formatted[k] = f"{v:.2f} {unit}" if unit else v
        return formatted

def calcular(parametros):
    return CicloBraytonRecalentamiento().calcular(parametros)