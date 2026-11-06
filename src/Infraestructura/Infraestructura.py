class Infraestructura():
    COSTES = {
        "Puente": {"Madera": 10, "Piedra": 10},
        "Castillo": {"Piedra": 50, "Hierro": 30, "Agua": 20},
        "Muralla": {"Piedra": 30},
        "Granja": {"Madera": 15, "Agua": 35},
        "Mina": {"Madera": 10, "Hierro": 10, "Agua": 10},
    }

    def __init__(self, tipo: str, eficiencia: int = 100):
        self.tipo = tipo
        self.eficiencia = eficiencia
        self._coste = self.COSTES.get(tipo, {})


    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def eficiencia(self) -> int:
        return self._eficiencia

    @property
    def coste(self) -> dict:
        return self._coste


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
        self.eficiencia -= 10
        return True

    def reparar(self, recursos_colonia: dict) -> bool:
        #Calculamos el coste de reparación (50% de los recursos necesarios para su creacion)
        coste_reparacion = {}
        for nombre_recurso, cant_original in self.coste.items():
            mitad_cantidad = int(cant_original / 2)
            if mitad_cantidad < 1:
                mitad_cantidad = 1
            coste_reparacion[nombre_recurso] = mitad_cantidad

        coste_original = self._coste
        self._coste = coste_reparacion

        #Comprobamos si la colonia tiene lo necesario
        if not self.comprobar_recursos(recursos_colonia):
            print(f"No hay suficientes recursos en la colonia para reparar '{self.tipo}'.")
            self._coste = coste_original
            return False

        #Descontamos los recursos
        for recurso_req, cantidad_req in coste_reparacion.items():
            recursos_colonia[recurso_req] -= cantidad_req

        self._coste = coste_original
        self.eficiencia = 100
        print(f"'{self.tipo}' ha sido reparada al 100% de eficiencia.")
        return True