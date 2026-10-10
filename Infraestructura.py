from Recursos import Recursos

class Infraestructura():
    lista_infra = ["Puente", "Castillo", "Muralla", "Granja"]
    COSTES = {
        "Puente": {"Madera": 20, "Piedra": 10},
        "Castillo": {"Piedra": 50, "Hierro": 30, "Agua": 20},
        "Muralla": {"Piedra": 30},
        "Granja": {"Madera": 15, "Agua": 35}
    }

    def __init__(self, tipo: str, eficiencia: int):
        self.tipo = tipo
        self.eficiencia = eficiencia
        self.coste = self.COSTES[self.tipo]


    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def eficiencia(self) -> int:
        return self._eficiencia

    @property
    def coste(self) -> list[Recursos]:
        return self._coste


    @tipo.setter
    def tipo(self, nuevo_tipo :str):
        if nuevo_tipo in self.lista_infra:
            self._tipo = nuevo_tipo
        else:
            raise ValueError(f"'{nuevo_tipo}' no es un tipo de infraestructura válido. Opciones: {self.lista_infra}")
    
    @eficiencia.setter
    def eficiencia(self, nueva_efic :int):
        if nueva_efic < 0 or nueva_efic > 100:
            raise ValueError(f"Eficiencia inválida ({nueva_efic}). Debe valer entre 0 y 100.")
        else:
            self._eficiencia = nueva_efic

    def mostrar_coste(self):
        print(f"Para construir la infraestructura '{self.tipo}' necesitas:")
        for recurso, cantidad in self.coste.items():
            print(f"\t- {recurso}|{cantidad}")

    def comprobar_recursos(self, recursos_colonia: list) -> bool:
        for recurso_req, cantidad_req in self.coste.items():
            recurso_encontrado = None
            #busca los recursos necesarios de COSTES en los recursos de la colonia
            for rec in recursos_colonia:
                if rec.tipo == recurso_req:
                    recurso_encontrado = rec
                    break
            #si la colonia no tiene el recurso
            if recurso_encontrado is None:
                return False
            #si el recurso no es suficiente
            if recurso_encontrado.cantidad < cantidad_req:
                return False
        return True
    
    # def construir(self, recurso: Recursos): 
    # falta definir este metodo
