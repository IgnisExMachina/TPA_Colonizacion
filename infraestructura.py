class Infraestructura():
    lista_infra = ["Puente", "Castillo", "Muralla", "Granja"]
    def __init__(self, tipo :str, eficiencia :int): #falta agregar coste
        self.tipo = tipo
        self.eficiencia = eficiencia
    
    @property
    def tipo(self):
        return self._tipo

    @property
    def eficiencia(self):
        return self._eficiencia

    @tipo.setter
    def tipo(self, nuevo_tipo :str):
        if nuevo_tipo in self.lista_infra:
            self._tipo = nuevo_tipo
        else:
            raise ValueError(f"'{nuevo_tipo}' no es un tipo de infraestructura válido. Opciones: {self.lista_infra}")
    
    @eficiencia.setter
    def eficiencia(self, nueva_efic :int):
        if nueva_efic > 0 or nueva_efic < 100:
            self._eficiencia = nueva_efic
        else:
            raise ValueError(f"Eficiencia inválida ({nueva_efic}). Debe valer entre 0 y 100.")