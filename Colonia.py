from Colono import Colono
from infraestructura import Infraestructura #CAMBIAR LA MAYÚSCULA DE INFRAESTRUCTURAS
from Recursos import Recursos


class Colonia:
    def __init__(self, nombreColonia: str, colonos: list = None, recursos: list = None, infraestructuras: list = None):
        if colonos is None and recursos is None and infraestructuras is None:
            self.colonos = []
            self.recursos = []
            self.infraestructuras = []
        else:
            self.colonos = colonos
            self.recursos = recursos
            self.infraestructuras = infraestructuras

        self.nombreColonia = nombreColonia

    def agregarColono(self, colono: Colono):
        self.colonos.append(colono)

    def verColonos(self): #! PONERLO MÁS BONITO CADA COLONO
        for colono in self.colonos:
            print(colono.nombre)

    def agregarRecurso(self, recurso: Recursos):
        self.recursos.append(recurso)

    def verRecursos(self):
        for recurso in self.recursos:
            print(recurso.tipo)
            print(recurso.cantidad)


    @property #getter
    def nombreColonia(self):
        return self.nombreColonia

    @nombreColonia.setter
    def nombreColonia(self, nombreColonia: str):
        self._nombreColonia = nombreColonia

    
    






#PRUEBAS---------------------

colono = Colono( "Dani", "kukusclan", 19, 3, "M")

print(colono.nombre)

colonia1 = Colonia("Kukusclan colonia", None, None, None)
colonia1.agregarColono(colono)
colonia1.verColonos()