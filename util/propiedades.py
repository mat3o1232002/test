# Funciones para manejo de propiedades con CoolProp
import CoolProp.CoolProp as CP  # Ensure CoolProp is installed: pip install CoolProp

class PropiedadesTermodinamicas:
    FLUIDOS_DISPONIBLES = [
        "Water", "Air", "Ammonia", "R134a", "R245fa",
        "Nitrogen", "CO2", "Helium", "Methane", "Hydrogen",
        "Propane", "Ethanol"
    ]

    def __init__(self, fluido="Water"):
        """Inicializar con el fluido especificado (Water por defecto)"""
        self.set_fluido(fluido)

    def set_fluido(self, fluido):
        """Validar y establecer el fluido"""
        if fluido not in self.FLUIDOS_DISPONIBLES:
            raise ValueError(f"Fluido '{fluido}' no soportado. Opciones: {', '.join(self.FLUIDOS_DISPONIBLES)}")
        self.fluido = fluido

    def propiedades_estado(self, p_bar=None, t_c=None, h_kjkg=None, s_kjkgK=None):
        """
        Obtener múltiples propiedades en un estado termodinámico
        Args:
            p_bar: Presión en bar
            t_c: Temperatura en °C
            h_kjkg: Entalpía en kJ/kg
            s_kjkgK: Entropía en kJ/kg-K
            
        Returns:
            Diccionario con todas las propiedades calculadas
        """
        p_pa = p_bar * 1e5 if p_bar is not None else None
        t_k = t_c + 273.15 if t_c is not None else None
        h_jkg = h_kjkg * 1000 if h_kjkg is not None else None
        # s_jkgK = s_kjkgK * 1000 if s_kjkgK is not None else None  # Removed unused variable

        props = {}
        
        try:
            if p_bar is not None and t_c is not None:
                props.update({
                    'h': CP.PropsSI('H', 'P', p_pa, 'T', t_k, self.fluido) / 1000,  # kJ/kg
                    's': CP.PropsSI('S', 'P', p_pa, 'T', t_k, self.fluido) / 1000,  # kJ/kg-K
                    'rho': CP.PropsSI('D', 'P', p_pa, 'T', t_k, self.fluido),  # kg/m³
                    'phase': CP.PhaseSI('P', p_pa, 'T', t_k, self.fluido)
                })
            elif p_bar is not None and h_kjkg is not None:
                props.update({
                    'T': CP.PropsSI('T', 'P', p_pa, 'H', h_jkg, self.fluido) - 273.15,  # °C
                    's': CP.PropsSI('S', 'P', p_pa, 'H', h_jkg, self.fluido) / 1000,    # kJ/kg-K
                    'rho': CP.PropsSI('D', 'P', p_pa, 'H', h_jkg, self.fluido),         # kg/m³
                    'phase': CP.PhaseSI('P', p_pa, 'H', h_jkg, self.fluido)
                })
            # Puedes añadir más combinaciones según necesites
            
            return props
            
        except Exception as e:
            raise ValueError(f"Error al calcular propiedades: {str(e)}")

    # Métodos específicos (pueden usarse como atajos)
    def entalpia(self, p_bar, t_c):
        """Obtener entalpía en kJ/kg"""
        return self.propiedades_estado(p_bar=p_bar, t_c=t_c)['h']

    def entropia(self, p_bar, t_c):
        """Obtener entropía en kJ/kg-K"""
        return self.propiedades_estado(p_bar=p_bar, t_c=t_c)['s']

    def temperatura(self, p_bar, h_kjkg):
        """Obtener temperatura en °C"""
        return self.propiedades_estado(p_bar=p_bar, h_kjkg=h_kjkg)['T']