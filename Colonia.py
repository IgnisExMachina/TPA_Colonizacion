from Colono import Colono
from Infraestructura import Infraestructura
from Recursos import Recursos


class Colonia:
    def __init__(self, nombre: str, colonos: list = None, recursos: list = None, infraestructuras: list = None):
        if colonos is None and recursos is None and infraestructuras is None:
            self.colonos = []
            self.recursos = []
            self.infraestructuras = []
        else:
            self.colonos = colonos
            self.recursos = recursos
            self.infraestructuras = infraestructuras

        self.nombre = nombre

    def agregarColono(self, colono: Colono):
        self.colonos.append(colono)

    def verColonos(self): #! PONERLO MÁS BONITO CADA COLONO
        for colono in self.colonos:
            print(colono)

    def agregarRecurso(self, recurso: Recursos):
        self.recursos.append(recurso)

    def verRecursos(self):
        for recurso in self.recursos:
            print(recurso.tipo)
            print(recurso.cantidad)

    def agregarInfraestructuras(self, infraestructura: Infraestructura):
        self.infraestructuras.append(infraestructura)

    def verInfraestructuras(self):
        for infraestructura in self.infraestructuras:
            print(infraestructura.tipo)
            print(infraestructura.eficiencia)


    @property #getter
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str):
        self._nombre = nombre

    
    






#PRUEBAS---------------------