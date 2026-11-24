class Infraestructura():
    # Costes de construccion. Las infraestructuras basicas son baratas para poder arrancar la colonia;
    # despues se mejoran "invirtiendo" en ellas (ver invertir()).
    COSTES = {
        "Aserradero": {"Madera": 10, "Piedra": 5},
        "Pozo": {"Piedra": 10, "Madera": 5},
        "Mina": {"Madera": 15, "Agua": 10},
        "Huerto": {"Madera": 10, "Agua": 5},
        "Granja": {"Madera": 15, "Agua": 35},
        "Muralla": {"Piedra": 25, "Madera": 10},
        "ExtractorDePlutonio": {"Hierro": 25, "Piedra": 20, "Madera": 15},
        "Castillo": {"Piedra": 50, "Hierro": 30, "Agua": 20},
    }
    MAX_NIVEL = 5
    FACTOR_INVERSION = 0.6   # invertir cuesta 60% del coste de construccion por cada nivel que ya tiene
    nivel = 1                # valor por defecto (tambien para infraestructuras de partidas antiguas)

    def __init__(self, tipo: str, eficiencia: int = 100):
        self.tipo = tipo
        self.eficiencia = eficiencia
        self.nivel = 1


    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def eficiencia(self) -> int:
        return self._eficiencia

    @property
    def coste(self) -> dict:
        # El coste sale siempre de COSTES segun el tipo. Asi no hace falta guardarlo en la partida
        # y las infraestructuras cargadas de un JSON lo tienen igual que las recien construidas.
        return self.COSTES.get(self.tipo, {})

    @coste.setter
    def coste(self, _valor):
        # Las partidas antiguas guardaban "coste"; al cargarlas se ignora (se recalcula desde COSTES)
        pass


    @tipo.setter
    def tipo(self, nuevo_tipo: str):
        if not isinstance(nuevo_tipo, str):
            raise TypeError("El tipo de infraestructura debe ser una cadena de texto.")
        if nuevo_tipo in self.COSTES:
            self._tipo = nuevo_tipo
        else:       
            raise ValueError(f"'{nuevo_tipo}' no es un tipo de infraestructura válido. Opciones: {list(self.COSTES.keys())}")
    
    @eficiencia.setter
    def eficiencia(self, nueva_efic: int):
        if not isinstance(nueva_efic, int):
            raise TypeError("La eficiencia debe ser un numero entero.")
        if nueva_efic < 0 or nueva_efic > 100:
            raise ValueError(f"Eficiencia inválida ({nueva_efic}). Debe valer entre 0 y 100.")
        else:
            self._eficiencia = nueva_efic

    @staticmethod
    def mostrar_todos_costes():
        newstr = ""
        for tipo in Infraestructura.COSTES:
            newstr += f"\n\t{tipo} | {' '.join(f'{recurso} - {Infraestructura.COSTES[tipo][recurso]}' for recurso in Infraestructura.COSTES[tipo])}"
        return newstr
    
    def mostrar_coste(self):
        print(f"Para construir la infraestructura '{self.tipo}' necesitas:")
        for recurso, cantidad in self.coste.items():
            print(f"\t- {recurso}|{cantidad}")

    def comprobar_recursos(self, recursos_colonia: dict) -> bool:
        if not isinstance(recursos_colonia, dict):
            raise TypeError("Los recursos de la colonia deben ser un diccionario.")
        for recurso_req, cantidad_req in self.coste.items():
            if recurso_req not in recursos_colonia or recursos_colonia[recurso_req] < cantidad_req:
                return False
        return True    
    
    def construir(self, recursos_colonia: dict) -> bool:
        if not self.comprobar_recursos(recursos_colonia):
            print(f"No hay suficientes recursos en la colonia para construir {self.tipo}.")
            return False
        
        for recurso_req, cantidad_req in self.coste.items():
            recursos_colonia[recurso_req] -= cantidad_req

        print(f"¡{self.tipo} construida con éxito!")
        print("Recursos utilizados:")
        for recurso_req, cantidad_req in self.coste.items():
            print(f"\t- {recurso_req}|{cantidad_req}")
        return True

    def aplicar_efecto(self, colonia) -> bool:
        if self.eficiencia == 0:
            print(f"{self.tipo} en {colonia.nombre} está destruida/inoperativa (0% de eficiencia). Requiere reparación.")
            return False
        self.eficiencia = max(0, self.eficiencia - 10)  # las averias pueden dejarla en 5, 45... y no puede bajar de 0
        return True

    # ---------- Inversion (subir de nivel) ----------
    def multiplicador(self) -> float:
        """Cuanto produce respecto al nivel 1: Nv1 x1, Nv2 x1.5, Nv3 x2, Nv4 x2.5, Nv5 x3."""
        return 1 + 0.5 * (self.nivel - 1)

    def descripcion_mejora(self) -> str:
        """Texto que explica que gana la infraestructura con su nivel actual."""
        return f"produce x{self.multiplicador():g}"

    def puede_invertir(self) -> bool:
        return self.nivel < self.MAX_NIVEL

    def coste_inversion(self) -> dict:
        """Cada nivel cuesta mas que el anterior."""
        return {recurso: max(1, round(cantidad * self.FACTOR_INVERSION * self.nivel))
                for recurso, cantidad in self.coste.items()}

    def invertir(self, recursos_colonia: dict) -> bool:
        """Gasta recursos para subir un nivel: produce mas y vuelve al 100% de eficiencia."""
        if not self.puede_invertir():
            print(f"'{self.tipo}' ya está al nivel máximo ({self.MAX_NIVEL}).")
            return False
        coste = self.coste_inversion()
        if not self._hay_recursos(recursos_colonia, coste):
            print(f"No hay suficientes recursos para invertir en '{self.tipo}'.")
            return False
        for recurso, cantidad in coste.items():
            recursos_colonia[recurso] -= cantidad
        self.nivel += 1
        self.eficiencia = 100
        print(f"Inversión con éxito: '{self.tipo}' sube a nivel {self.nivel} ({self.descripcion_mejora()}).")
        return True

    # ---------- Reparacion ----------
    def coste_reparacion(self) -> dict:
        """Reparar cuesta el 50% de los recursos necesarios para construirla (minimo 1 de cada)."""
        return {recurso: max(1, int(cantidad / 2)) for recurso, cantidad in self.coste.items()}

    def reparar(self, recursos_colonia: dict) -> bool:
        coste_reparacion = self.coste_reparacion()

        #Comprobamos si la colonia tiene lo necesario
        if not self._hay_recursos(recursos_colonia, coste_reparacion):
            print(f"No hay suficientes recursos en la colonia para reparar '{self.tipo}'.")
            return False

        #Descontamos los recursos
        for recurso_req, cantidad_req in coste_reparacion.items():
            recursos_colonia[recurso_req] -= cantidad_req

        self.eficiencia = 100
        print(f"'{self.tipo}' ha sido reparada al 100% de eficiencia.")
        return True

    @staticmethod
    def _hay_recursos(recursos_colonia: dict, coste: dict) -> bool:
        return all(recursos_colonia.get(recurso, 0) >= cantidad for recurso, cantidad in coste.items())

Infraestructura.mostrar_todos_costes()
